from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Review, Title
from users.models import User

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from review.csv"

    def handle(self, *args, **options):
        if Review.objects.exists():
            print('review data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print("Loading review data")
        for row in DictReader(open(
            'static/data/review.csv',
            encoding='utf-8'
        )):
            review = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()
