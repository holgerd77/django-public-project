import os
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from public_project.models import Document

class Command(BaseCommand):
    
    args = '<document_id>'
    help = 'Used internally to generate images from pdf document pages'
    
    def handle(self, *args, **options):
        for document_id in args:
            try:
                document = Document.objects.get(pk=int(document_id))
            except Document.DoesNotExist:
                raise CommandError('Document "%s" does not exist' % document_id)
            if document.page_set.count() > 0:
                raise CommandError('Pages for document "%s" already created' % document_id)
            
            #Create images
            pdf_path = os.path.join(settings.MEDIA_ROOT, unicode(document.document))
            path = document.get_pages_path()
            if not os.path.exists(path):
                os.makedirs(path)
            
            cmd = u"convert -quality 90 -density 100 '"  + pdf_path + "' '" + path + "page-%d.png'"
            p = subprocess.Popen(cmd, shell=True)
            retval = p.wait()
            document.pdf_images_generated = True
            document.save()
            