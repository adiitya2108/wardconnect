--
-- PostgreSQL database dump
--

\restrict vJUgXBMCapHqr8yYWCYQNbgQ3CrpcNIZnmkKFsdxRFgUmUNflk4BU3xwYIXIXWZ

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    admin_id character varying(20) NOT NULL,
    name character varying(50),
    email character varying(50),
    password character varying(255)
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: complaint; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaint (
    complaint_id character varying(20) NOT NULL,
    user_id character varying(20),
    ward_id character varying(20),
    category character varying(30),
    title character varying(100),
    description text,
    photo character varying(250),
    latitude numeric(10,7),
    longitude numeric(10,7),
    complaint_date timestamp without time zone,
    status character varying(20),
    resolution_proof character varying(250),
    resolution_remark text,
    resolution_date date,
    address text
);


ALTER TABLE public.complaint OWNER TO postgres;

--
-- Name: corporator; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.corporator (
    corporator_id character varying(20) NOT NULL,
    admin_id character varying(20),
    name character varying(50),
    mobile character varying(11),
    email character varying(50),
    ward_id character varying(20),
    role character varying(20),
    password character varying(255)
);


ALTER TABLE public.corporator OWNER TO postgres;

--
-- Name: feedback; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feedback (
    feedback_id character varying(20) NOT NULL,
    complaint_id character varying(20),
    user_id character varying(20),
    rating integer,
    comment text,
    feedback_date date
);


ALTER TABLE public.feedback OWNER TO postgres;

--
-- Name: resident; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resident (
    user_id character varying(20) NOT NULL,
    full_name character varying(50),
    mobile character varying(11),
    email character varying(50),
    password character varying(300),
    ward_id character varying(20),
    address text,
    pincode character varying(10),
    user_type character varying(20)
);


ALTER TABLE public.resident OWNER TO postgres;

--
-- Name: verification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.verification (
    verification_id character varying(20) NOT NULL,
    user_id character varying(20),
    doc_type character varying(50),
    doc_number character varying(50),
    doc_photo character varying(250),
    status character varying(20),
    verified_by character varying(20),
    verified_date date,
    rejection_reason text
);


ALTER TABLE public.verification OWNER TO postgres;

--
-- Name: ward; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ward (
    ward_id character varying(20) NOT NULL,
    ward_no integer,
    ward_name character varying(50),
    area character varying(100),
    pincode character varying(10),
    corporator_id character varying(20)
);


ALTER TABLE public.ward OWNER TO postgres;

--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin (admin_id, name, email, password) FROM stdin;
ADM001	Super Admin	admin@wardconnect.com	scrypt:32768:8:1$Qofd9ROWYg228EeT$bf1db3fae86bcd52bab56d5c6594fa8676b0f61dc0ac03ad0ecce4be5e7f1aa2e056a72771682da5f7325db32b5d3c9cac50a96902728eceee4ba00e926f60a4
\.


--
-- Data for Name: complaint; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaint (complaint_id, user_id, ward_id, category, title, description, photo, latitude, longitude, complaint_date, status, resolution_proof, resolution_remark, resolution_date, address) FROM stdin;
WC77B2D5	UB7DAAE	W05	Road	no roads	0 roads in town	uploads/2c8757_Capture6nov2.PNG	18.5377970	73.8517458	2026-11-08 11:52:38.915112	Resolved	\N	who cares	2026-11-09	\N
\.


--
-- Data for Name: corporator; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.corporator (corporator_id, admin_id, name, mobile, email, ward_id, role, password) FROM stdin;
CORP101	ADM001	XYZ Corporator	9876543210	corrupted@ward.com	W05	Corporator	scrypt:32768:8:1$f5KOXE2saRwA7DeN$c435967c2d63b476c780cf2b9131b28d2889ac2dcd536f0e58a470b044411ced016e4311c4d7b2a539d24a08715bdd4fcd0494362fbe53f52f42cdbc76952b2c
CORP102	ADM001	P sharma	9876500000	p@ward.com	W06	Corporator	scrypt:32768:8:1$6RZVNNCPyifb4KvR$289c0c39d60713b4b4300543d66c6fe4ce2c9d989ccccaa1a978a688d16fe55b6cf22553715d3ab36b425a5c03b07cff65d5b34e3c41716e145f22792e4cc4c9
\.


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feedback (feedback_id, complaint_id, user_id, rating, comment, feedback_date) FROM stdin;
F75D462	WC77B2D5	UB7DAAE	1	fake 	2026-11-09
\.


--
-- Data for Name: resident; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resident (user_id, full_name, mobile, email, password, ward_id, address, pincode, user_type) FROM stdin;
UB7DAAE	Aditya Prakash Ankush	8010167604	adityaankush002@gmail.com	scrypt:32768:8:1$QfFh4uKiMUYpi46O$edd0d91b56bc4135caf2037163e58d6d7642a3febf2321bfad2087af8dc4896d7a6d10270e05c15a762581b8080eeaaac646fdf4c38287359c7809e33d7f4d8b	W05	8/247 shivajinagar pune	411003	Permanent
\.


--
-- Data for Name: verification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.verification (verification_id, user_id, doc_type, doc_number, doc_photo, status, verified_by, verified_date, rejection_reason) FROM stdin;
V7998E7	UB7DAAE	Aadhaar	758966547112	uploads/062c60_pexels-therato-17684642.jpg	Approved	CORP101	2026-11-09	\N
\.


--
-- Data for Name: ward; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ward (ward_id, ward_no, ward_name, area, pincode, corporator_id) FROM stdin;
W05	5	Kothrud	Kothrud Area	411038	\N
W06	\N	Kothrud West	Kothrud city xy	411009	\N
\.


--
-- Name: admin admin_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_email_key UNIQUE (email);


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (admin_id);


--
-- Name: complaint complaint_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint
    ADD CONSTRAINT complaint_pkey PRIMARY KEY (complaint_id);


--
-- Name: corporator corporator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.corporator
    ADD CONSTRAINT corporator_pkey PRIMARY KEY (corporator_id);


--
-- Name: feedback feedback_complaint_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_complaint_id_key UNIQUE (complaint_id);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (feedback_id);


--
-- Name: resident resident_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resident
    ADD CONSTRAINT resident_email_key UNIQUE (email);


--
-- Name: resident resident_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resident
    ADD CONSTRAINT resident_pkey PRIMARY KEY (user_id);


--
-- Name: verification verification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.verification
    ADD CONSTRAINT verification_pkey PRIMARY KEY (verification_id);


--
-- Name: ward ward_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ward
    ADD CONSTRAINT ward_pkey PRIMARY KEY (ward_id);


--
-- Name: ward ward_ward_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ward
    ADD CONSTRAINT ward_ward_no_key UNIQUE (ward_no);


--
-- Name: complaint complaint_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint
    ADD CONSTRAINT complaint_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.resident(user_id);


--
-- Name: complaint complaint_ward_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint
    ADD CONSTRAINT complaint_ward_id_fkey FOREIGN KEY (ward_id) REFERENCES public.ward(ward_id);


--
-- Name: corporator corporator_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.corporator
    ADD CONSTRAINT corporator_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public.admin(admin_id);


--
-- Name: corporator corporator_ward_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.corporator
    ADD CONSTRAINT corporator_ward_id_fkey FOREIGN KEY (ward_id) REFERENCES public.ward(ward_id);


--
-- Name: feedback feedback_complaint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_complaint_id_fkey FOREIGN KEY (complaint_id) REFERENCES public.complaint(complaint_id);


--
-- Name: feedback feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.resident(user_id);


--
-- Name: resident resident_ward_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resident
    ADD CONSTRAINT resident_ward_id_fkey FOREIGN KEY (ward_id) REFERENCES public.ward(ward_id);


--
-- Name: verification verification_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.verification
    ADD CONSTRAINT verification_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.resident(user_id);


--
-- Name: ward ward_corporator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ward
    ADD CONSTRAINT ward_corporator_id_fkey FOREIGN KEY (corporator_id) REFERENCES public.corporator(corporator_id);


--
-- PostgreSQL database dump complete
--

\unrestrict vJUgXBMCapHqr8yYWCYQNbgQ3CrpcNIZnmkKFsdxRFgUmUNflk4BU3xwYIXIXWZ

