CREATE SCHEMA IF NOT EXISTS content;

SET search_path TO content,public; 

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    file_path TEXT,
    rating FLOAT,
    type TEXT NOT NULL,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL references content.film_work(id) ON DELETE CASCADE,
    person_id uuid NOT NULL references content.person(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created_at timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL references content.film_work(id) ON DELETE CASCADE,
    genre_id uuid NOT NULL references content.genre(id) ON DELETE CASCADE,
    created_at timestamp with time zone
);


CREATE INDEX person_film_work_role_idx ON content.person_film_work(role);
CREATE INDEX film_work_rating_idx ON content.film_work(rating);
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date); 
CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (genre_id, film_work_id);