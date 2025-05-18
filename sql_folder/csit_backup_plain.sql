--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-14 21:06:42

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

DROP DATABASE csit314;
--
-- TOC entry 4946 (class 1262 OID 24623)
-- Name: csit314; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE csit314 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en-GB';


ALTER DATABASE csit314 OWNER TO postgres;

\connect csit314

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

--
-- TOC entry 6 (class 2615 OID 24624)
-- Name: csit314_schma; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA csit314_schma;


ALTER SCHEMA csit314_schma OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 227 (class 1259 OID 24702)
-- Name: feedback; Type: TABLE; Schema: csit314_schma; Owner: postgres
--

CREATE TABLE csit314_schma.feedback (
    feedback_id bigint NOT NULL,
    username text DEFAULT 'anonymous'::text,
    phone_number text DEFAULT 'anonymous'::text,
    feedback_text text
);


ALTER TABLE csit314_schma.feedback OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 24701)
-- Name: feedback_feedback_id_seq; Type: SEQUENCE; Schema: csit314_schma; Owner: postgres
--

CREATE SEQUENCE csit314_schma.feedback_feedback_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE csit314_schma.feedback_feedback_id_seq OWNER TO postgres;

--
-- TOC entry 4947 (class 0 OID 0)
-- Dependencies: 226
-- Name: feedback_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: csit314_schma; Owner: postgres
--

ALTER SEQUENCE csit314_schma.feedback_feedback_id_seq OWNED BY csit314_schma.feedback.feedback_id;


--
-- TOC entry 219 (class 1259 OID 24626)
-- Name: general_user; Type: TABLE; Schema: csit314_schma; Owner: postgres
--

CREATE TABLE csit314_schma.general_user (
    user_id bigint NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    email text NOT NULL,
    phone_number text NOT NULL,
    address text,
    is_cleaner boolean NOT NULL,
    service_id_list bigint[],
    profile_description text,
    picture_url text,
    preferences jsonb
);


ALTER TABLE csit314_schma.general_user OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24625)
-- Name: general_user_user_id_seq; Type: SEQUENCE; Schema: csit314_schma; Owner: postgres
--

CREATE SEQUENCE csit314_schma.general_user_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE csit314_schma.general_user_user_id_seq OWNER TO postgres;

--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 218
-- Name: general_user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: csit314_schma; Owner: postgres
--

ALTER SEQUENCE csit314_schma.general_user_user_id_seq OWNED BY csit314_schma.general_user.user_id;


--
-- TOC entry 223 (class 1259 OID 24651)
-- Name: payment; Type: TABLE; Schema: csit314_schma; Owner: postgres
--

CREATE TABLE csit314_schma.payment (
    payment_id bigint NOT NULL,
    service_id bigint NOT NULL,
    from_user_id bigint NOT NULL,
    to_user_id bigint NOT NULL,
    price numeric(2,2),
    payment_timestamp timestamp(3) with time zone,
    booking_timestamp timestamp(3) with time zone
);


ALTER TABLE csit314_schma.payment OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 24650)
-- Name: payment_payment_id_seq; Type: SEQUENCE; Schema: csit314_schma; Owner: postgres
--

CREATE SEQUENCE csit314_schma.payment_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE csit314_schma.payment_payment_id_seq OWNER TO postgres;

--
-- TOC entry 4949 (class 0 OID 0)
-- Dependencies: 222
-- Name: payment_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: csit314_schma; Owner: postgres
--

ALTER SEQUENCE csit314_schma.payment_payment_id_seq OWNED BY csit314_schma.payment.payment_id;


--
-- TOC entry 225 (class 1259 OID 24673)
-- Name: review; Type: TABLE; Schema: csit314_schma; Owner: postgres
--

CREATE TABLE csit314_schma.review (
    review_id bigint NOT NULL,
    review_score smallint,
    review_text text,
    by_user_id bigint,
    service_id bigint
);


ALTER TABLE csit314_schma.review OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 24672)
-- Name: review_review_id_seq; Type: SEQUENCE; Schema: csit314_schma; Owner: postgres
--

CREATE SEQUENCE csit314_schma.review_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE csit314_schma.review_review_id_seq OWNER TO postgres;

--
-- TOC entry 4950 (class 0 OID 0)
-- Dependencies: 224
-- Name: review_review_id_seq; Type: SEQUENCE OWNED BY; Schema: csit314_schma; Owner: postgres
--

ALTER SEQUENCE csit314_schma.review_review_id_seq OWNED BY csit314_schma.review.review_id;


--
-- TOC entry 221 (class 1259 OID 24637)
-- Name: service; Type: TABLE; Schema: csit314_schma; Owner: postgres
--

CREATE TABLE csit314_schma.service (
    service_id bigint NOT NULL,
    service_name text NOT NULL,
    by_user_id bigint NOT NULL,
    price numeric(2,2),
    duration text,
    service_description text,
    service_tags text[],
    picture_url text[],
    listing_timestamp timestamp(3) with time zone
);


ALTER TABLE csit314_schma.service OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24636)
-- Name: service_service_id_seq; Type: SEQUENCE; Schema: csit314_schma; Owner: postgres
--

CREATE SEQUENCE csit314_schma.service_service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE csit314_schma.service_service_id_seq OWNER TO postgres;

--
-- TOC entry 4951 (class 0 OID 0)
-- Dependencies: 220
-- Name: service_service_id_seq; Type: SEQUENCE OWNED BY; Schema: csit314_schma; Owner: postgres
--

ALTER SEQUENCE csit314_schma.service_service_id_seq OWNED BY csit314_schma.service.service_id;


--
-- TOC entry 4767 (class 2604 OID 24705)
-- Name: feedback feedback_id; Type: DEFAULT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.feedback ALTER COLUMN feedback_id SET DEFAULT nextval('csit314_schma.feedback_feedback_id_seq'::regclass);


--
-- TOC entry 4763 (class 2604 OID 24629)
-- Name: general_user user_id; Type: DEFAULT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.general_user ALTER COLUMN user_id SET DEFAULT nextval('csit314_schma.general_user_user_id_seq'::regclass);


--
-- TOC entry 4765 (class 2604 OID 24654)
-- Name: payment payment_id; Type: DEFAULT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.payment ALTER COLUMN payment_id SET DEFAULT nextval('csit314_schma.payment_payment_id_seq'::regclass);


--
-- TOC entry 4766 (class 2604 OID 24676)
-- Name: review review_id; Type: DEFAULT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.review ALTER COLUMN review_id SET DEFAULT nextval('csit314_schma.review_review_id_seq'::regclass);


--
-- TOC entry 4764 (class 2604 OID 24640)
-- Name: service service_id; Type: DEFAULT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.service ALTER COLUMN service_id SET DEFAULT nextval('csit314_schma.service_service_id_seq'::regclass);


--
-- TOC entry 4940 (class 0 OID 24702)
-- Dependencies: 227
-- Data for Name: feedback; Type: TABLE DATA; Schema: csit314_schma; Owner: postgres
--

COPY csit314_schma.feedback (feedback_id, username, phone_number, feedback_text) FROM stdin;
\.


--
-- TOC entry 4932 (class 0 OID 24626)
-- Dependencies: 219
-- Data for Name: general_user; Type: TABLE DATA; Schema: csit314_schma; Owner: postgres
--

COPY csit314_schma.general_user (user_id, username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, "picture)url") FROM stdin;
\.


--
-- TOC entry 4936 (class 0 OID 24651)
-- Dependencies: 223
-- Data for Name: payment; Type: TABLE DATA; Schema: csit314_schma; Owner: postgres
--

COPY csit314_schma.payment (payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp) FROM stdin;
\.


--
-- TOC entry 4938 (class 0 OID 24673)
-- Dependencies: 225
-- Data for Name: review; Type: TABLE DATA; Schema: csit314_schma; Owner: postgres
--

COPY csit314_schma.review (review_id, review_score, review_text, by_user_id, service_id) FROM stdin;
\.


--
-- TOC entry 4934 (class 0 OID 24637)
-- Dependencies: 221
-- Data for Name: service; Type: TABLE DATA; Schema: csit314_schma; Owner: postgres
--

COPY csit314_schma.service (service_id, service_name, by_user_id, price, duration, service_description, service_tags, picture_url) FROM stdin;
\.


--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 226
-- Name: feedback_feedback_id_seq; Type: SEQUENCE SET; Schema: csit314_schma; Owner: postgres
--

SELECT pg_catalog.setval('csit314_schma.feedback_feedback_id_seq', 1, false);


--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 218
-- Name: general_user_user_id_seq; Type: SEQUENCE SET; Schema: csit314_schma; Owner: postgres
--

SELECT pg_catalog.setval('csit314_schma.general_user_user_id_seq', 1, false);


--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 222
-- Name: payment_payment_id_seq; Type: SEQUENCE SET; Schema: csit314_schma; Owner: postgres
--

SELECT pg_catalog.setval('csit314_schma.payment_payment_id_seq', 1, false);


--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 224
-- Name: review_review_id_seq; Type: SEQUENCE SET; Schema: csit314_schma; Owner: postgres
--

SELECT pg_catalog.setval('csit314_schma.review_review_id_seq', 1, false);


--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 220
-- Name: service_service_id_seq; Type: SEQUENCE SET; Schema: csit314_schma; Owner: postgres
--

SELECT pg_catalog.setval('csit314_schma.service_service_id_seq', 1, false);


--
-- TOC entry 4777 (class 2606 OID 24656)
-- Name: payment pk_payment_id; Type: CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.payment
    ADD CONSTRAINT pk_payment_id PRIMARY KEY (payment_id);


--
-- TOC entry 4779 (class 2606 OID 24680)
-- Name: review pk_reviewID; Type: CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.review
    ADD CONSTRAINT "pk_reviewID" PRIMARY KEY (review_id);


--
-- TOC entry 4775 (class 2606 OID 24644)
-- Name: service pk_serviceID; Type: CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.service
    ADD CONSTRAINT "pk_serviceID" PRIMARY KEY (service_id);


--
-- TOC entry 4771 (class 2606 OID 24633)
-- Name: general_user pk_userID; Type: CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.general_user
    ADD CONSTRAINT "pk_userID" PRIMARY KEY (user_id);


--
-- TOC entry 4773 (class 2606 OID 24635)
-- Name: general_user unique_email; Type: CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.general_user
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- TOC entry 4781 (class 2606 OID 24657)
-- Name: payment payment_from to user; Type: FK CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.payment
    ADD CONSTRAINT "payment_from to user" FOREIGN KEY (from_user_id) REFERENCES csit314_schma.general_user(user_id);


--
-- TOC entry 4782 (class 2606 OID 24667)
-- Name: payment payment_service to service; Type: FK CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.payment
    ADD CONSTRAINT "payment_service to service" FOREIGN KEY (service_id) REFERENCES csit314_schma.service(service_id);


--
-- TOC entry 4783 (class 2606 OID 24662)
-- Name: payment payment_to to user; Type: FK CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.payment
    ADD CONSTRAINT "payment_to to user" FOREIGN KEY (to_user_id) REFERENCES csit314_schma.general_user(user_id);


--
-- TOC entry 4784 (class 2606 OID 24681)
-- Name: review review_by_user_id to user; Type: FK CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.review
    ADD CONSTRAINT "review_by_user_id to user" FOREIGN KEY (by_user_id) REFERENCES csit314_schma.general_user(user_id);


--
-- TOC entry 4785 (class 2606 OID 24686)
-- Name: review review_service_id to service; Type: FK CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.review
    ADD CONSTRAINT "review_service_id to service" FOREIGN KEY (service_id) REFERENCES csit314_schma.service(service_id);


--
-- TOC entry 4780 (class 2606 OID 24645)
-- Name: service service_creator to user; Type: FK CONSTRAINT; Schema: csit314_schma; Owner: postgres
--

ALTER TABLE ONLY csit314_schma.service
    ADD CONSTRAINT "service_creator to user" FOREIGN KEY (by_user_id) REFERENCES csit314_schma.general_user(user_id) ON DELETE CASCADE;


-- Completed on 2025-05-14 21:06:42

--
-- PostgreSQL database dump complete
--

