from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Genre, Title

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):
        print("Loading genre data")
        for row in DictReader(
                open('api_yamdb/static/data/genre_title.csv', encoding='utf-8')
        ):
            title = Title.objects.get(id=row['title_id'])
            title.genre.add(Genre.objects.get(id=row['genre_id']))
