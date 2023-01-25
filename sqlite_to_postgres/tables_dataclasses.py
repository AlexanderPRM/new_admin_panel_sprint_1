import datetime
import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    file_path: str
    rating: float
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass(frozen=True)
class GenreFilmWork:
    id: uuid.UUID
    genre_id: uuid.UUID
    filmwork_id: uuid.UUID
    created_at: datetime.datetime


@dataclass(frozen=True)
class PersonFilmWork:
    id: uuid.UUID
    filmwork_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.datetime
