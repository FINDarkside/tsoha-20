# CEATE TABLE kyselyt

```SQL

CREATE TABLE public.account
(
    id integer NOT NULL DEFAULT nextval('account_id_seq'::regclass),
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    is_admin boolean NOT NULL,
    CONSTRAINT account_pkey PRIMARY KEY (id)
)

CREATE INDEX ix_account_username
    ON public.account USING btree
    (username COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
```

## Feature

```SQL
CREATE TABLE public.feature
(
    id integer NOT NULL DEFAULT nextval('feature_id_seq'::regclass),
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    user_id integer,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default" NOT NULL,
    category_id integer,
    CONSTRAINT feature_pkey PRIMARY KEY (id),
    CONSTRAINT feature_category_id_fkey FOREIGN KEY (category_id)
        REFERENCES public.feature_category (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE INDEX ix_feature_category_id
    ON public.feature USING btree
    (category_id ASC NULLS LAST)
    TABLESPACE pg_default;
```

## FeatureCategory

```SQL
CREATE TABLE public.feature_category
(
    id integer NOT NULL DEFAULT nextval('feature_category_id_seq'::regclass),
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT feature_category_pkey PRIMARY KEY (id)
)
```

## Like

```SQL
CREATE TABLE public."like"
(
    id integer NOT NULL DEFAULT nextval('like_id_seq'::regclass),
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    user_id integer NOT NULL,
    feature_id integer NOT NULL,
    CONSTRAINT like_pkey PRIMARY KEY (id),
    CONSTRAINT like_feature_id_fkey FOREIGN KEY (feature_id)
        REFERENCES public.feature (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT like_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.account (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE INDEX ix_like_feature_id
    ON public."like" USING btree
    (feature_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX ix_like_user_id
    ON public."like" USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;
```
