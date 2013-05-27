import urllib2
from django.test import TestCase
from django.utils.translation import ugettext as _  
from fixtures.project_factory import ProjectFactory as PF
from public_project.models import *


TEST_SERVER_URL = 'http://127.0.0.1:8010'
API_VERSION = 'v0.1'

class APITest(TestCase):
    """
    Tests for the different api endpoints for general functionality
    """
    def test_documents_end_point(self):
        PF.create_base_project()
        url = '%s/api/%s/%s?format=json' % (TEST_SERVER_URL, API_VERSION, 'documents/')
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"title":'), 1, "Documents api end point not working!")
    
    def test_document_end_point(self):
        PF.create_base_project()
        d = Document.objects.all()[0]
        url = '%s/api/%s/%s%i/?format=json' % (TEST_SERVER_URL, API_VERSION, 'documents/', d.pk)
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"title":'), 1, "Document api end point not working!")
    
    def test_events_end_point(self):
        PF.create_base_project()
        url = '%s/api/%s/%s?format=json' % (TEST_SERVER_URL, API_VERSION, 'events/')
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"title":'), 1, "Events api end point not working!")
    
    def test_event_end_point(self):
        PF.create_base_project()
        e = Event.objects.all()[0]
        url = '%s/api/%s/%s%i/?format=json' % (TEST_SERVER_URL, API_VERSION, 'events/', e.pk)
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"title":'), 1, "Event api end point not working!")
    
    def test_participants_end_point(self):
        PF.create_base_project()
        url = '%s/api/%s/%s?format=json' % (TEST_SERVER_URL, API_VERSION, 'participants/')
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"name":'), 1, "Participants api end point not working!")
    
    def test_participant_end_point(self):
        PF.create_base_project()
        p = Participant.objects.all()[0]
        url = '%s/api/%s/%s%i/?format=json' % (TEST_SERVER_URL, API_VERSION, 'participants/', p.pk)
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"name":'), 1, "Participant api end point not working!")
    
    def test_project_parts_end_point(self):
        PF.create_base_project()
        url = '%s/api/%s/%s?format=json' % (TEST_SERVER_URL, API_VERSION, 'project_parts/')
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"name":'), 1, "Project parts api end point not working!")
    
    def test_project_part_end_point(self):
        PF.create_base_project()
        pp = ProjectPart.objects.all()[0]
        url = '%s/api/%s/%s%i/?format=json' % (TEST_SERVER_URL, API_VERSION, 'project_parts/', pp.pk)
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"name":'), 1, "Project part end point not working!")
    
    def test_questions_end_point(self):
        PF.create_base_project()
        url = '%s/api/%s/%s?format=json' % (TEST_SERVER_URL, API_VERSION, 'questions/')
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"title":'), 1, "Questions api end point not working!")
    
    def test_question_end_point(self):
        PF.create_base_project()
        q = Question.objects.all()[0]
        url = '%s/api/%s/%s%i/?format=json' % (TEST_SERVER_URL, API_VERSION, 'questions/', q.pk)
        response = urllib2.urlopen(url)
        json = response.read()
        self.assertGreaterEqual(json.count('"title":'), 1, "Question api end point not working!")
    