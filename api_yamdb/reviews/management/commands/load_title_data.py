from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Title

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):
        if Title.objects.exists():
            print('title data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print("Loading title data")
        for row in DictReader(open(
            'static/data/titles.csv',
            encoding='utf-8'
        )):
            title = Title(
                id=row['titid'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])
            )
            title.save()
