from core.models import TimeStampedMixin, UUIDMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(verbose_name=_("fullname"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self) -> str:
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        movie = ("movie", "MOVIE")
        tv_show = ("tv_show", "TV SHOW")

    title = models.TextField(verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"), blank=True)
    creation_date = models.DateField(
        verbose_name=_("creation_date"), auto_now_add=True
    )
    file_path = models.FileField(
        _("file"), blank=True, null=True, upload_to="movies/"
    )
    rating = models.FloatField(
        verbose_name=_("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        verbose_name=_("type"), max_length=255, choices=FilmType.choices
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")
    persons = models.ManyToManyField(Person, through="PersonFilmWork")

    class Meta:
        db_table = 'content"."film_work'
        indexes = (
            models.Index(fields=['rating'], name='film_work_rating_idx'),
            models.Index(
                fields=['creation_date'], name='film_work_creation_date_idx'
                ))
        verbose_name = _("filmwork")
        verbose_name_plural = _("filmworks")

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork", verbose_name=_("filmwork"), on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        "Genre", verbose_name=_("genre"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        constraints = (models.UniqueConstraint(
            fields=['film_work_id', 'genre_id'],
            name='film_work_person_idx'),)
        verbose_name = _("film genre")
        verbose_name_plural = _("film genres")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork", verbose_name=_("filmwork"), on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        "Person", verbose_name=_("person"), on_delete=models.CASCADE
    )
    role = models.TextField(verbose_name=_("role"), null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        indexes = (models.Index(
            fields=['role'],
            name='person_film_work_role_idx'),)
        verbose_name = _("participant film")
        verbose_name_plural = _("participants film")
