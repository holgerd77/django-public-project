from django.core.management.base import BaseCommand
from fixtures.project_factory import ProjectFactory

class Command(BaseCommand):
    help = 'Creates the example data for the example project'

    def handle(self, *args, **options):
        pf = ProjectFactory()
        pf.create_base_project()
