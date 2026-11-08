import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template,request,redirect,session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from config import DB_HOST , DB_NAME , DB_USER, DB_PASSWORD , DB_PORT
import uuid
from datetime import datetime


app = Flask(__name__)
app.secret_key = "wardconnect_secret"
app.config["UPLOAD_FOLDER"] = "static/uploads"

def get_db():
	return psycopg2.connect(
	host=DB_HOST,
	database=DB_NAME,
	user=DB_USER,
	password=DB_PASSWORD,
	port=DB_PORT

	)

@app.route("/")
def home():
	return render_template("index.html")


@app.route("/register" , methods=["GET","POST"])
def register():
	if request.method == "POST":
		full_name = request.form["full_name"]
		mobile = request.form["mobile"]
		email = request.form["email"]
		password = generate_password_hash(request.form["password"])
		ward_id = request.form["ward_id"]
		address = request.form["address"]
		pincode = request.form["pincode"]
		user_type = request.form["user_type"]
		user_id = "U" + uuid.uuid4().hex[:6].upper()

		conn = get_db()
		cur = conn.cursor()
		cur.execute("INSERT INTO resident (user_id,full_name,mobile,email,password,ward_id,address,pincode,user_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								(user_id,full_name,mobile,email,password,ward_id,address,pincode,user_type))
		conn.commit()
		cur.close()
		conn.close()
		return redirect("/")
	return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		conn = get_db()
		cur = conn.cursor()
		cur.execute("SELECT user_id,full_name,password FROM resident WHERE email = %s",(email,))
		user = cur.fetchone()
		cur.close()
		conn.close()

		if user and check_password_hash(user[2],password):
			session["user_id"] = user[0]
			session["full_name"] = user[1]
			return redirect("/")
		else:
			return "Invalid Email Or Password . <a href='/login'>Try Again </a> "
	return render_template("login.html")

@app.route("/verification",methods=["GET","POST"])
def verification():
	if  "user_id" not in session:
		return redirect("/login")

	if request.method == "POST":
		user_id = session["user_id"]

		#Check Duplicate Verification Submissions
		conn = get_db()
		cur = conn.cursor()
		cur.execute("SELECT status FROM verification WHERE user_id = %s" , (user_id,))
		existing = cur.fetchone()
		cur.close()
		conn.close()
		if existing and existing[0] in ("Pending","Approved"):
			return f"Verification Already Submitted ! Status : {existing[0]}. <a href''/'> Back To Home </a> "

		doc_type = request.form["doc_type"]
		doc_number = request.form["doc_number"]
		file = request.files["doc_photo"]

		filename = uuid.uuid4().hex[:6] + "_" + secure_filename(file.filename)
		file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
		doc_photo = "uploads/" + filename

		verification_id = "V" + uuid.uuid4().hex[:6].upper()

		conn = get_db()
		cur = conn.cursor()
		cur.execute("INSERT INTO verification (verification_id , user_id , doc_type , doc_number ,  doc_photo , status ) VALUES (%s ,%s ,%s , %s , %s , %s)",
								(verification_id , user_id , doc_type , doc_number , doc_photo , "Pending"))
		conn.commit()
		cur.close()
		conn.close()
		return "Verification Submitted ! Status : Pending, <a href='/'> Back to Home </a>"
	return render_template("verification.html")
 

@app.route("/complaint",methods=["GET","POST"])
def complaint():
	if "user_id" not in session:
		return redirect("/login")

	if request.method == "POST":
		user_id = session["user_id"]
		category = request.form["category"]
		title = request.form["title"]
		description = request.form["description"]
		address = request.form.get("address") or None 

		lat = request.form.get("latitude") or None
		lon = request.form.get("longitude") or None
		latitude = float(lat) if lat else None
		longitude = float(lon) if lon else None
		if not address and not latitude and not longitude:
			return "Please Provide either Auto GPS or Manual Address <a href ='/complaint' >Try Agian</a>"

		conn = get_db()
		cur = conn.cursor()
		cur.execute("SELECT ward_id FROM resident WHERE user_id = %s",(user_id,))
		row = cur.fetchone()
		ward_id = row[0] if row else None

		file = request.files["photo"]
		filename = uuid.uuid4().hex[:6] + "_" + secure_filename(file.filename)
		file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
		photo = "uploads/" + 	 filename

		complaint_id = "WC" + uuid.uuid4().hex[:6].upper()

		cur.execute("INSERT INTO complaint (complaint_id,user_id,ward_id,category,title,description,photo,latitude,longitude,complaint_date,status, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								(complaint_id,user_id,ward_id,category,title,description,photo,latitude,longitude,datetime.now(),"Pending", address))
		conn.commit()
		cur.close()
		conn.close()
		return "complaint Submitted ! Status : Pending . <a href='/'> Back to home </a>"

	return render_template("post_complaint.html")

@app.route("/my_complaints")
def my_complaints():
	if "user_id" not in session:
		return redirect("/login")

	user_id = session["user_id"]

	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT complaint_id,title,category,status,complaint_date FROM complaint WHERE  	user_id = %s ORDER BY  complaint_date DESC", (user_id,))
	complaints = cur.fetchall()
	cur.close()
	conn.close()

	return render_template("my_complaints.html", complaints=complaints ) 

if __name__ == "__main__":
	app.run(debug=True)