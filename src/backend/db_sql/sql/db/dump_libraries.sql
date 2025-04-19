--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    id integer NOT NULL,
    book_uid uuid NOT NULL,
    name character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    genre character varying(255) NOT NULL,
    condition character varying(20),
    CONSTRAINT book_condition_check CHECK (((condition)::text = ANY (ARRAY[('EXCELLENT'::character varying)::text, ('GOOD'::character varying)::text, ('BAD'::character varying)::text])))
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_id_seq OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_id_seq OWNED BY public.book.id;


--
-- Name: library; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library (
    id integer NOT NULL,
    library_uid uuid NOT NULL,
    name character varying(80) NOT NULL,
    city character varying(255) NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.library OWNER TO postgres;

--
-- Name: library_book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library_book (
    id integer NOT NULL,
    book_id integer,
    library_id integer,
    available_count integer NOT NULL
);


ALTER TABLE public.library_book OWNER TO postgres;

--
-- Name: library_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.library_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.library_book_id_seq OWNER TO postgres;

--
-- Name: library_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.library_book_id_seq OWNED BY public.library_book.id;


--
-- Name: library_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.library_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.library_id_seq OWNER TO postgres;

--
-- Name: library_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.library_id_seq OWNED BY public.library.id;


--
-- Name: book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);


--
-- Name: library id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library ALTER COLUMN id SET DEFAULT nextval('public.library_id_seq'::regclass);


--
-- Name: library_book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book ALTER COLUMN id SET DEFAULT nextval('public.library_book_id_seq'::regclass);


--
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book (id, book_uid, name, author, genre, condition) FROM stdin;
3	f7cdc58f-2caf-4b15-9727-f89dcc629b28	Гарри Поттер и узник Азкабана	Джоан Роулинг	Научная фантастика	EXCELLENT
7	f7cdc58f-2caf-4b15-9727-f89dcc629b33	1984	Джордж Оруэлл	Утопия	EXCELLENT
8	f7cdc58f-2caf-4b15-9727-f89dcc629b34	Гарри Поттер и философский камень	Джоан Роулинг	Научная фантастика	EXCELLENT
10	f7cdc58f-2caf-4b15-9727-f89dcc629b36	Великий Гэтсби	Ф. С. Фицджеральд	Триллер	EXCELLENT
11	f7cdc58f-2caf-4b15-9727-f89dcc629b37	Паутина Шарлотты	Элвин Брукс Уайт	Детектив	EXCELLENT
6	f7cdc58f-2caf-4b15-9727-f89dcc629b32	Дневник Анны Франк	Анна Франк	Автобиография	EXCELLENT
9	f7cdc58f-2caf-4b15-9727-f89dcc629b35	Властелин колец	Дж. Р. Р. Толкин	Научная фантастика	GOOD
1	f7cdc58f-2caf-4b15-9727-f89dcc629b27	Краткий курс C++ в 7 томах	Бьерн Страуструп	Научная фантастика	EXCELLENT
5	f7cdc58f-2caf-4b15-9727-f89dcc629b31	Гордость и предубеждение	Джейн Остен	Триллер	EXCELLENT
4	f7cdc58f-2caf-4b15-9727-f89dcc629b29	Убить пересмешника	Харпер Ли	Детектив	EXCELLENT
\.


--
-- Data for Name: library; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library (id, library_uid, name, city, address) FROM stdin;
1	83575e12-7ce0-48ee-9931-51919ff3c9ee	Библиотека имени 7 Непьющих	Москва	2-я Бауманская ул., д.5, стр.1
2	3062a61f-b125-4b17-8374-a7ce97efaf28	Центральная бибилотека	Москва	Бригадирский переулок
38	3062a61f-b125-4b17-8374-a7ce97efaf29	Царская библиотека	Санкт-Питербург	Дворцовая площадь
39	3062a61f-b125-4b17-8374-a7ce97efaf30	Российская государственная библиотека	Москва	Никольская улица
40	3062a61f-b125-4b17-8374-a7ce97efaf31	Российская национальная библиотека	Санкт-Питербург	Литейный проспект
41	3062a61f-b125-4b17-8374-a7ce97efaf32	Библиотека Российской академии наук	Санкт-Питербург	Думская улица
42	3062a61f-b125-4b17-8374-a7ce97efaf33	Институт научной информации по общественным наукам Российской академии наук	Москва	Арбат
44	3062a61f-b125-4b17-8374-a7ce97efaf35	Научная библиотека Казанского (Приволжского) федерального университета	Казань	Улица Баумана
45	3062a61f-b125-4b17-8374-a7ce97efaf36	Донская государственная публичная библиотека	Ростов-на-Дону	Улица Максима Горького
43	3062a61f-b125-4b17-8374-a7ce97efaf34	Государственная публичная техническая библиотека Сибирского отделения России	Новосибирск	Улица Титова
\.


--
-- Data for Name: library_book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library_book (id, book_id, library_id, available_count) FROM stdin;
3	3	1	0
6	6	1	10
7	7	1	0
10	10	1	0
9	9	1	3
1	1	1	27
12	5	2	12
4	4	1	7
11	11	1	10
8	8	1	6
13	6	2	111
5	5	1	1
\.


--
-- Name: book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_id_seq', 11, true);


--
-- Name: library_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_book_id_seq', 13, true);


--
-- Name: library_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_id_seq', 45, true);


--
-- Name: book book_book_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_book_uid_key UNIQUE (book_uid);


--
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- Name: library_book library_book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_pkey PRIMARY KEY (id);


--
-- Name: library library_library_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_library_uid_key UNIQUE (library_uid);


--
-- Name: library library_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_name_key UNIQUE (name);


--
-- Name: library library_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_pkey PRIMARY KEY (id);


--
-- Name: ix_book_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_book_id ON public.book USING btree (id);


--
-- Name: ix_library_book_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_library_book_id ON public.library_book USING btree (id);


--
-- Name: ix_library_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_library_id ON public.library USING btree (id);


--
-- Name: library_book library_book_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: library_book library_book_library_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_library_id_fkey FOREIGN KEY (library_id) REFERENCES public.library(id);


--
-- PostgreSQL database dump complete
--

