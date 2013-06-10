import urllib2
from django.test import TestCase
from django.utils.translation import ugettext as _  
from fixtures.project_factory import ProjectFactory as PF
from public_project.models import *


TEST_SERVER_URL = 'http://127.0.0.1:8010'

class RSSTest(TestCase):
    """
    Tests for the different rss feeds related to the frontend website for general functionality
    """    
    def test_main_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/rss/' % (TEST_SERVER_URL))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 5, "Main rss feed not working!")
    
    def test_project_parts_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%srss/' % (TEST_SERVER_URL, _('project_parts_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Project parts rss feed not working!")
    
    def test_questions_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%srss/' % (TEST_SERVER_URL, _('questions_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Questions rss feed not working!")
    
    def test_participants_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%srss/' % (TEST_SERVER_URL, _('participants_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Participants rss feed not working!")
    
    def test_process_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%srss/' % (TEST_SERVER_URL, _('events_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Events rss feed not working!")
    
    def test_research_requests_of_question_feed(self):
        PF.create_base_project()
        q = Question.objects.all()[0]
        response = urllib2.urlopen('%s/%s%i/%srss/' % (TEST_SERVER_URL, _('questions_url'), q.pk, _('research_requests_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Research Requests of question rss feed not working!")
    
    def test_research_requests_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%s%srss/' % (TEST_SERVER_URL, _('questions_url'), _('research_requests_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Research Requests rss feed not working!")
    
    def test_comments_of_content_object_feed(self):
        PF.create_base_project()
        p1 = Participant.objects.all()[0]
        c1 = Comment.objects.all()[0]
        response = urllib2.urlopen('%s/%s%i/%srss/' % (TEST_SERVER_URL, _('participants_url'), c1.pk, _('comments_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Comments of content object rss feed not working!")
    
    def test_comments_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%srss/' % (TEST_SERVER_URL, _('comments_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Comments rss feed not working!")
    
    def test_documents_feed(self):
        PF.create_base_project()
        response = urllib2.urlopen('%s/%srss/' % (TEST_SERVER_URL, _('documents_url')))
        xml = response.read()
        self.assertGreaterEqual(xml.count('<item>'), 1, "Documents rss feed not working!")
    