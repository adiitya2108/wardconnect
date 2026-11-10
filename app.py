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

@app.route("/corporator_login",methods=["GET","POST"])
def corporator_login():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		conn = get_db()
		cur = conn.cursor()
		cur.execute	("SELECT corporator_id,ward_id,password FROM corporator WHERE email = %s ", (email,))
		corp = cur.fetchone()
		cur.close()
		conn.close()

		if corp and check_password_hash(corp[2],password):
			session["corporator_id"] = corp[0]
			session["ward_id"] = corp[1]
			session["role"] = "corporator"
			return redirect("/corporator_dashboard")
		else:
			return "Invalid corporator email or password . <a href='/corporator_login'>Try Again</a>"
	return render_template("corporator_login.html")

@app.route("/corporator_dashboard")
def corporator_dashboard():
	if "corporator_id" not in session:
		return redirect("/corporator_login")

	ward_id = session["ward_id"]

	conn = get_db()
	cur = conn.cursor()
	#only pending verifications of my ward
	cur.execute("SELECT v.verification_id, v.user_id , v.doc_type , v.doc_number , v.doc_photo FROM verification v JOIN resident r ON v.user_id  = r.user_id WHERE v.status = 'Pending' AND r.ward_id = %s ",(ward_id,))
	verifications = cur.fetchall()
	#all cmp of this ward
	cur.execute("SELECT	complaint_id , title , category , status FROM complaint WHERE ward_id = %s ORDER BY complaint_date DESC ", (ward_id,))
	complaints = cur.fetchall()
	cur.close()
	conn.close()

	return render_template("corporator_dashboard.html", ward_id=ward_id , verifications=verifications, complaints=complaints)

@app.route("/verify/<verification_id>/approve", methods=["POST"])
def approve_verification(verification_id):
	if "corporator_id" not in session:
		return redirect("/corporator_login")

	conn = get_db()
	cur = conn.cursor()
	cur.execute("UPDATE verification SET status = 'Approved', verified_by = %s,verified_date = CURRENT_DATE , rejection_reason = NULL WHERE verification_id = %s",(session["corporator_id"],verification_id))
	conn.commit()
	cur.close()
	conn.close()
	return redirect("/corporator_dashboard")

@app.route("/verify/<verification_id>/reject", methods=["POST"])
def reject_verification(verification_id):
	if "corporator_id" not in session:
		return redirect("/corporator_login")

	reason = request.form.get("rejection_reason") or "No reason given."

	conn = get_db()
	cur = conn.cursor()
	cur.execute("UPDATE verification SET status = 'Rejected' , verified_by =  %s, verified_date = CURRENT_DATE , rejection_reason = %s WHERE verification_id = %s ",(session["corporator_id"],reason,verification_id))
	conn.commit()
	cur.close()
	conn.close()
	return redirect("/corporator_dashboard")

@app.route("/complaint/<complaint_id>/status",methods=["POST"])
def update_complaint_status(complaint_id):
	if "corporator_id" not in session:
		return redirect("/corporator_login")

	new_status = request.form["status"]
	remark = request.form.get("resolution_remark") or None

	conn = get_db()
	cur = conn.cursor()
	if new_status == "Resolved":
		cur.execute("UPDATE complaint SET status = %s,resolution_remark = %s ,resolution_date = CURRENT_DATE WHERE complaint_id = %s" ,(new_status,remark,complaint_id))
	else:
		cur.execute("UPDATE complaint SET status = %s, resolution_remark = %s WHERE complaint_id = %s" ,(new_status ,remark, complaint_id))
	conn.commit()
	cur.close()
	conn.close()
	return	redirect("/corporator_dashboard")


@app.route("/feedback/<complaint_id>",methods=["GET","POST"])
def give_feedback(complaint_id):
	if "user_id" not in session:
		return redirect("/login")

	if request.method == "POST":
		rating = request.form["rating"]
		comment = request.form.get("comment") or None

		conn = get_db()
		cur = conn.cursor()

		cur.execute("SELECT feedback_id FROM feedback WHERE complaint_id = %s",(complaint_id,))
		existing = cur.fetchone()
		if existing:
			cur.close()
			conn.close()
			return "feedback Already given for this complaint. <a href = '/my_complaints'> Go Back</a> "

		cur.execute("SELECT user_id from  complaint WHERE complaint_id = %s",(complaint_id,))
		owner = cur.fetchone()
		if not owner  or owner[0] != session["user_id"]:
			cur.close()
			conn.close()
			return "You cannot submit feedback for this complaint"

		feedback_id = "F" + uuid.uuid4().hex[:6].upper()
		cur.execute("INSERT INTO feedback (feedback_id,complaint_id,user_id,rating,comment,feedback_date) VALUES (%s,%s,%s,%s,%s,%s )",
								(feedback_id,complaint_id,session["user_id"],rating,comment,datetime.now()))
		conn.commit()
		cur.close()
		conn.close()
		return redirect("/my_complaints")

	return render_template("feedback.html",complaint_id=complaint_id)

@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		conn = get_db()
		cur = conn.cursor()
		cur.execute("SELECT admin_id,password FROM admin WHERE email	 = %s ", (email,))
		adm = cur.fetchone()
		cur.close()
		conn.close()

		if adm and check_password_hash(adm[1],password):
			session["admin_id" ] = adm[0]
			session["role"] = "admin"
			return redirect("/admin_dashboard")
		else:
			return "Invalid Email or Password . <a href = '/admin_login' >Try Again </a>"

	return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
	if "admin_id" not in session:
		return redirect("/admin_login")

	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT ward_id,ward_name,area,pincode FROM ward ORDER BY ward_id ")
	wards = cur.fetchall()
	cur.execute("SELECT complaint_id,title,ward_id,status FROM complaint ORDER 	BY complaint_date DESC")
	complaints = cur.fetchall()
	cur.execute("SELECT corporator_id, name, email, ward_id,role FROM corporator ORDER BY corporator_id ")
	corporators = cur.fetchall()
	cur.execute("SELECT feedback_id, complaint_id , rating, comment FROM feedback ORDER BY feedback_date DESC")
	feedbacks = cur.fetchall()
	cur.close()
	conn.close()

	return render_template("admin_dashboard.html",wards=wards,corporators=corporators,complaints=complaints,feedbacks=feedbacks)


# --- ADD WARD ---
@app.route("/add_ward", methods=["GET", "POST"])
def add_ward():
    if request.method == "POST":
        ward_id = request.form.get("ward_id")
        ward_name = request.form.get("ward_name")
        area = request.form.get("area")
        pincode = request.form.get("pincode")

        conn = sqlite3.connect("wardconnect.db")
        cur = conn.cursor()
        # Create table if not exists
        cur.execute("CREATE TABLE IF NOT EXISTS wards (ward_id TEXT PRIMARY KEY, ward_name TEXT, area TEXT, pincode TEXT)")
        cur.execute("INSERT INTO wards (ward_id, ward_name, area, pincode) VALUES (?, ?, ?, ?)", (ward_id, ward_name, area, pincode))
        conn.commit()
        conn.close()
        return redirect("/admin_dashboard")
    return render_template("add_ward.html")

# --- ADD CORPORATOR ---
@app.route("/add_corporator", methods=["GET", "POST"])
def add_corporator():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        mobile = request.form.get("mobile")
        ward_id = request.form.get("ward_id")

        conn = sqlite3.connect("wardconnect.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS corporators (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, email TEXT, password TEXT, mobile TEXT, ward_id TEXT)")
        cur.execute("INSERT INTO corporators (full_name, email, password, mobile, ward_id) VALUES (?, ?, ?, ?, ?)", (full_name, email, password, mobile, ward_id))
        conn.commit()
        conn.close()
        return redirect("/admin_dashboard")
    return render_template("add_corporator.html")


# @app.route("/admin/add_ward", methods=["POST"])
# def admin_add_ward():
# 	if "admin_id" not in session:
# 		return redirect("/admin_login")

# 	ward_id = request.form["ward_id"]
# 	ward_name = request.form["ward_name"]
# 	area = request.form.get("area") or None
# 	pincode = request.form.get("pincode") or None

# 	conn = get_db()
# 	cur = conn.cursor()
# 	cur.execute("INSERT INTO ward (ward_id,ward_name,area,pincode) VALUES (%s,%s,%s,%s)",(ward_id,ward_name,area,pincode))
# 	conn.commit()
# 	cur.close()
# 	conn.close()
# 	return redirect("/admin_dashboard")

# @app.route("/admin/add_corporator", methods=["POST"])
# def admin_add_corporator():
# 	if "admin_id" not in session:
# 		return redirect("/admin_login")

# 	corporator_id = request.form["corporator_id"]
# 	name = request.form["name"]
# 	mobile = request.form["mobile"]
# 	email = request.form["email"]
# 	ward_id = request.form["ward_id"]
# 	role = request.form["role"]
# 	password = generate_password_hash(request.form["password"])

# 	conn = get_db()
# 	cur = conn.cursor()
# 	cur.execute("INSERT INTO corporator (corporator_id,admin_id ,name,mobile,email,ward_id,role,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
# 								(corporator_id,session["admin_id"],name,mobile,email,ward_id,role,password))
# 	conn.commit()
# 	cur.close()
# 	conn.close()
# 	return redirect("/admin_dashboard")



if __name__ == "__main__":
	app.run(debug=True)