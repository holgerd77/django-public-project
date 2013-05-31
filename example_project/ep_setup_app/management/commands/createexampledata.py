from django.core.management.base import BaseCommand, CommandError
from ep_setup_app.example_data import ExampleData

class Command(BaseCommand):
    help = 'Creates the example data for the example project'

    def handle(self, *args, **options):
        ed = ExampleData()
        ed.create()
