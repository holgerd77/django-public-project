from django.core.management.base import BaseCommand, CommandError
from public_project.models import Document
from public_project.doc_scanner import DocScanner
from public_project.tag_cache_creator import rebuild_cache_for_document

class Command(BaseCommand):
    
    args = '<document_id>'
    help = 'Used internally to generate pages from pdf documents'
    
    def handle(self, *args, **options):
        for document_id in args:
            try:
                document = Document.objects.get(pk=int(document_id))
            except Document.DoesNotExist:
                raise CommandError('Document "%s" does not exist' % document_id)
            document.page_set.all().delete()
            ds = DocScanner(document)
            ds.create_pages()
            
            rebuild_cache_for_document(document)
