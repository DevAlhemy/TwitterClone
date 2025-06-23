--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-23 15:30:01

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
-- TOC entry 4955 (class 1262 OID 16388)
-- Name: db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';


ALTER DATABASE db OWNER TO postgres;

\connect db

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
-- TOC entry 217 (class 1259 OID 16389)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 30314)
-- Name: follows; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.follows (
    follower_id integer NOT NULL,
    following_id integer NOT NULL
);


ALTER TABLE public.follows OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 30344)
-- Name: likes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.likes (
    user_id integer NOT NULL,
    tweet_id integer NOT NULL
);


ALTER TABLE public.likes OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 30291)
-- Name: medias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medias (
    id integer NOT NULL,
    file_path character varying NOT NULL
);


ALTER TABLE public.medias OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 30290)
-- Name: medias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.medias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medias_id_seq OWNER TO postgres;

--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 220
-- Name: medias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.medias_id_seq OWNED BY public.medias.id;


--
-- TOC entry 223 (class 1259 OID 30300)
-- Name: tweets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tweets (
    id integer NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tweets OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 30299)
-- Name: tweets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tweets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tweets_id_seq OWNER TO postgres;

--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 222
-- Name: tweets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tweets_id_seq OWNED BY public.tweets.id;


--
-- TOC entry 225 (class 1259 OID 30329)
-- Name: tweets_medias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tweets_medias (
    tweet_id integer NOT NULL,
    media_id integer NOT NULL
);


ALTER TABLE public.tweets_medias OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 30282)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    api_key character varying(100) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 30281)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 218
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4769 (class 2604 OID 30294)
-- Name: medias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias ALTER COLUMN id SET DEFAULT nextval('public.medias_id_seq'::regclass);


--
-- TOC entry 4770 (class 2604 OID 30303)
-- Name: tweets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets ALTER COLUMN id SET DEFAULT nextval('public.tweets_id_seq'::regclass);


--
-- TOC entry 4768 (class 2604 OID 30285)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4940 (class 0 OID 16389)
-- Dependencies: 217
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
5b889c822b8c
\.


--
-- TOC entry 4947 (class 0 OID 30314)
-- Dependencies: 224
-- Data for Name: follows; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.follows (follower_id, following_id) FROM stdin;
1	2
2	1
\.


--
-- TOC entry 4949 (class 0 OID 30344)
-- Dependencies: 226
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.likes (user_id, tweet_id) FROM stdin;
1	2
2	1
\.


--
-- TOC entry 4944 (class 0 OID 30291)
-- Dependencies: 221
-- Data for Name: medias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medias (id, file_path) FROM stdin;
1	1f53cc39-a3f2-4ccc-8940-94ac15216779.jpg
2	971c5a2b-2668-4b98-8117-fc123cf9a891.png
\.


--
-- TOC entry 4946 (class 0 OID 30300)
-- Dependencies: 223
-- Data for Name: tweets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tweets (id, user_id, content, created_at) FROM stdin;
1	1	First tweet!	2025-06-16 20:06:35.393612+07
2	2	O kak!	2025-06-16 20:06:35.424839+07
\.


--
-- TOC entry 4948 (class 0 OID 30329)
-- Dependencies: 225
-- Data for Name: tweets_medias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tweets_medias (tweet_id, media_id) FROM stdin;
1	1
2	2
\.


--
-- TOC entry 4942 (class 0 OID 30282)
-- Dependencies: 219
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, api_key) FROM stdin;
1	test	test
2	admin	admin
\.


--
-- TOC entry 4959 (class 0 OID 0)
-- Dependencies: 220
-- Name: medias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medias_id_seq', 3, false);


--
-- TOC entry 4960 (class 0 OID 0)
-- Dependencies: 222
-- Name: tweets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tweets_id_seq', 3, false);


--
-- TOC entry 4961 (class 0 OID 0)
-- Dependencies: 218
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, false);


--
-- TOC entry 4773 (class 2606 OID 16393)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4783 (class 2606 OID 30318)
-- Name: follows follows_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_pkey PRIMARY KEY (follower_id, following_id);


--
-- TOC entry 4787 (class 2606 OID 30348)
-- Name: likes likes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_pkey PRIMARY KEY (user_id, tweet_id);


--
-- TOC entry 4779 (class 2606 OID 30298)
-- Name: medias medias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias
    ADD CONSTRAINT medias_pkey PRIMARY KEY (id);


--
-- TOC entry 4785 (class 2606 OID 30333)
-- Name: tweets_medias tweets_medias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets_medias
    ADD CONSTRAINT tweets_medias_pkey PRIMARY KEY (tweet_id, media_id);


--
-- TOC entry 4781 (class 2606 OID 30308)
-- Name: tweets tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (id);


--
-- TOC entry 4775 (class 2606 OID 30289)
-- Name: users users_api_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_api_key_key UNIQUE (api_key);


--
-- TOC entry 4777 (class 2606 OID 30287)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4789 (class 2606 OID 30319)
-- Name: follows follows_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4790 (class 2606 OID 30324)
-- Name: follows follows_following_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_following_id_fkey FOREIGN KEY (following_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4793 (class 2606 OID 30354)
-- Name: likes likes_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_tweet_id_fkey FOREIGN KEY (tweet_id) REFERENCES public.tweets(id) ON DELETE CASCADE;


--
-- TOC entry 4794 (class 2606 OID 30349)
-- Name: likes likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4791 (class 2606 OID 30339)
-- Name: tweets_medias tweets_medias_media_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets_medias
    ADD CONSTRAINT tweets_medias_media_id_fkey FOREIGN KEY (media_id) REFERENCES public.medias(id) ON DELETE CASCADE;


--
-- TOC entry 4792 (class 2606 OID 30334)
-- Name: tweets_medias tweets_medias_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets_medias
    ADD CONSTRAINT tweets_medias_tweet_id_fkey FOREIGN KEY (tweet_id) REFERENCES public.tweets(id) ON DELETE CASCADE;


--
-- TOC entry 4788 (class 2606 OID 30309)
-- Name: tweets tweets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets
    ADD CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


-- Completed on 2025-06-23 15:30:01

--
-- PostgreSQL database dump complete
--

