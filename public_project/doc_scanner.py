#!/usr/bin/python

# Code taken from/based on https://github.com/Piratenfraktion-Berlin/PublicDocs
# thanks to Philip Brechler, @Plaetzchen

import os
from django.conf import settings
from django.utils.encoding import smart_unicode 

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure


class DocScanner():

    def __init__(self, document):
        self.document = document
        self.pdf_file = None
        try:
            self.pdf_path = os.path.join(settings.MEDIA_ROOT, unicode(self.document.document))
            self.pdf_file = open(self.pdf_path, 'rb')
        except IOError:
            # the file doesn't exist or similar problem
            pass
    
    
    def __del__(self):
        # close the pdf file
        if self.pdf_file:
            self.pdf_file.close()
    
    
    ###
    ### Extracting Images
    ###
    def write_file (self, folder, filename, filedata, flags='w'):
        """Write the file data to the folder and filename combination
        (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
        result = False
        if os.path.isdir(folder):
            try:
                file_obj = open(os.path.join(folder, filename), flags)
                file_obj.write(filedata)
                file_obj.close()
                result = True
            except IOError:
                pass
        return result
    
    
    ###
    ### Extracting Text
    ###
    def to_bytestring (self, s, enc='utf-8'):
        """Convert the given unicode string to a bytestring, using the standard encoding,
        unless it's already a bytestring"""
        if s:
            if isinstance(s, str):
                return s
            else:
                return s.encode(enc)
    
    
    def update_page_text_hash (self, h, lt_obj, pct=0.2):
        """Use the bbox x0,x1 values within pct% to produce lists of associated text within the hash"""
    
        x0 = lt_obj.bbox[0]
        x1 = lt_obj.bbox[2]
    
        key_found = False
        for k, v in h.items():
            hash_x0 = k[0]
            if x0 >= (hash_x0 * (1.0-pct)) and (hash_x0 * (1.0+pct)) >= x0:
                hash_x1 = k[1]
                if x1 >= (hash_x1 * (1.0-pct)) and (hash_x1 * (1.0+pct)) >= x1:
                    # the text inside this LT* object was positioned at the same
                    # width as a prior series of text, so it belongs together
                    key_found = True
                    v.append(self.to_bytestring(lt_obj.get_text()))
                    h[k] = v
        if not key_found:
            # the text, based on width, is a new series,
            # so it gets its own series (entry in the hash)
            h[(x0,x1)] = [self.to_bytestring(lt_obj.get_text())]
    
        return h
    
    
    def _parse_lt_objs (self, lt_objs, page_number, text=[]):
        """Iterate through the list of LT* objects and capture the text or image data contained in each"""
        text_content = [] 
    
        page_text = {} # k=(x0, x1) of the bbox, v=list of text strings within that bbox width (physical column)
        for lt_obj in lt_objs:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                # text, so arrange is logically based on its column width
                page_text = self.update_page_text_hash(page_text, lt_obj)
            elif isinstance(lt_obj, LTFigure):
                # LTFigure objects are containers for other LT* objects, so recurse through the children
                text_content.append(self._parse_lt_objs(lt_obj, page_number, text_content))
    
        for k, v in sorted([(key,value) for (key,value) in page_text.items()]):
            # sort the page_text hash by the keys (x0,x1 values of the bbox),
            # which produces a top-down, left-to-right sequence of related columns
            text_content.append(''.join(v))
    
        return '\n'.join(text_content)
    

    def _parse_pages (self, doc):
        """With an open PDFDocument object, get the pages and parse each one"""
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
    
        text_content = []
        for i, page in enumerate(doc.get_pages()):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            layout = device.get_result()
            # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
            text_content.append(self._parse_lt_objs(layout, (i+1)))
    
        return text_content

    
    def create_pages(self):
        """Apply parsing function, returning the results"""

        from public_project.models import Page
        # create a parser object associated with the file object
        parser = PDFParser(self.pdf_file)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument()
        # connect the parser and document objects
        parser.set_document(doc)
        doc.set_parser(parser)
        # supply the password for initialization
        pdf_pwd = ''
        doc.initialize(pdf_pwd)

        if doc.is_extractable:
            # apply the function and return the result
            doc_pages = self._parse_pages(doc)

        i = 1
        for doc_page in doc_pages:
            page = Page(
                document=self.document,
                number=i,
                content = smart_unicode(doc_page, encoding='utf-8', strings_only=False, errors='strict'),
            )
            page.save()
            i = i + 1
        
