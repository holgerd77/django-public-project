from django.core.management.base import BaseCommand
from public_project.models import SearchTag
from public_project.tag_cache_creator import rebuild_cache_for_tag


class Command(BaseCommand):
    
    args = ''
    help = 'Rebuilding of all search tag cache entries for the project'
    
    def handle(self, *args, **options):
        tags = SearchTag.objects.all()
        for tag in tags:
            print tag
            rebuild_cache_for_tag(tag)
