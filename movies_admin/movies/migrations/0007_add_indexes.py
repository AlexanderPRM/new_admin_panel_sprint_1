# Generated by Django 3.2 on 2023-01-26 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_rename_columns'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['rating'], name='film_work_rating_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['role'], name='person_film_work_role_idx'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='film_work_person_idx'),
        ),
    ]
