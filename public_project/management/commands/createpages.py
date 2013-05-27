from django.core.management.base import BaseCommand, CommandError
from public_project.models import Document
from public_project.doc_scanner import DocScanner

class Command(BaseCommand):
    
    args = '<document_id>'
    help = 'Used internally to generate pages from pdf documents'
    
    def handle(self, *args, **options):
        for document_id in args:
            try:
                document = Document.objects.get(pk=int(document_id))
            except Document.DoesNotExist:
                raise CommandError('Document "%s" does not exist' % document_id)
            if document.page_set.count() > 0:
                raise CommandError('Pages for document "%s" already created' % document_id)
            ds = DocScanner(document)
            ds.create_pages()
