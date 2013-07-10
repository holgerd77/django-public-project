import time
from django.test import LiveServerTestCase
from django.utils.translation import ugettext as _  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from fixtures.project_factory import ProjectFactory as PF
from public_project.models import *


SELENIUM_SLEEP_TIME = 1


class GenericTest(LiveServerTestCase):
    """
    Tests for the different pages of the frontend website for general functionality
    """
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(GenericTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(GenericTest, cls).tearDownClass()
    
    def test_main_page(self):
        PF.create_base_project()
        self.selenium.get('%s/' % (self.live_server_url))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//div[@id="site_intro_text"]')
        except NoSuchElementException:
            self.assertTrue(0, "No main page displayed!")
    
    def test_project_parts_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('project_parts_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + _("Topics") + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "No project page displayed!")
    
    def test_project_part_page(self):
        PF.create_base_project()
        pp = ProjectPart.objects.all()[0]
        self.selenium.get('%s/%s%i/' % (self.live_server_url, _('project_parts_url'), pp.pk))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h3[contains(text(),"' + pp.name + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Project part page not displayed correctly!")
    
    def test_questions_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('questions_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + _("Questions") + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "No questions page displayed!")
    
    def test_question_page(self):
        PF.create_base_project()
        q = Question.objects.all()[0]
        self.selenium.get('%s/%s%i/' % (self.live_server_url, _('questions_url'), q.pk))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h3[contains(text(),"' + q.title + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Question page not displayed correctly!")
    
    def test_participants_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('participants_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + _("Participants") + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "No participants page displayed!")
    
    def test_participant_page(self):
        PF.create_base_project()
        p = Participant.objects.all()[0]
        self.selenium.get('%s/%s%i/' % (self.live_server_url, _('participants_url'), p.pk))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h3[contains(text(),"' + p.name + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Participant page not displayed correctly!")
    
    def test_events_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('events_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + _("Events") + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "No process page displayed!")
    
    def test_event_page(self):
        PF.create_base_project()
        e = Event.objects.all()[0]
        self.selenium.get('%s/%s%i/' % (self.live_server_url, _('events_url'), e.pk))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h3[contains(text(),"' + e.title + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Event page not displayed correctly!")
    
    def test_display_research_request_on_question_page(self):
        PF.create_base_project()
        q = Question.objects.all()[0]
        rr = ResearchRequest.objects.all()[0]
        self.selenium.get('%s/%s%i/?research_request_id=%i' % (self.live_server_url, _('questions_url'), q.pk, rr.pk))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            x_path = '//div[@class="modal-header"]/h3[contains(text(),"' + _("Research Request") + '")]'
            self.selenium.find_element_by_xpath(x_path)
        except NoSuchElementException:
            self.assertTrue(0, "Research Request on question page not displayed correctly!")
    
    def test_research_requests_of_question_page(self):
        PF.create_base_project()
        q = Question.objects.all()[0]
        self.selenium.get('%s/%s%i/%s' % (self.live_server_url, _('questions_url'), q.pk, _('research_requests_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            x_path = '//h3[contains(text(),"' + q.title + '")]'
            self.selenium.find_element_by_xpath(x_path)
        except NoSuchElementException:
            self.assertTrue(0, "Research Requests of question page not displayed correctly!")
    
    def test_research_requests_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s%s' % (self.live_server_url, _('questions_url'), _('research_requests_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            x_path = '//div[@class="comment_header"]'
            self.selenium.find_element_by_xpath(x_path)
        except NoSuchElementException:
            self.assertTrue(0, "Research Requests page not displayed correctly!")
    
    def test_display_comment_on_content_object_page(self):
        PF.create_base_project()
        p1 = Participant.objects.all()[0]
        c1 = Comment.objects.all()[0]
        self.selenium.get('%s/%s%i/?comment_id=%i' % (self.live_server_url, _('participants_url'), p1.pk, c1.pk))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            x_path = '//div[@class="modal-header"]/h3[contains(text(),"' + _("Comment") + '")]'
            self.selenium.find_element_by_xpath(x_path)
        except NoSuchElementException:
            self.assertTrue(0, "Comment on content object page not displayed correctly!")
    
    def test_comments_of_content_object_page(self):
        PF.create_base_project()
        p1 = Participant.objects.all()[0]
        c1 = Comment.objects.all()[0]
        self.selenium.get('%s/%s%i/%s' % (self.live_server_url, _('participants_url'), p1.pk, _('comments_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            x_path = '//h3[contains(text(),"' + p1.name + '")]'
            self.selenium.find_element_by_xpath(x_path)
        except NoSuchElementException:
            self.assertTrue(0, "Comments of content object page not displayed correctly!")
    
    def test_comments_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('comments_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            x_path = '//div[@class="comment_header"]'
            self.selenium.find_element_by_xpath(x_path)
        except NoSuchElementException:
            self.assertTrue(0, "Comments page not displayed correctly!")
    
    def test_documents_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('documents_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + _("Documents") + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "No documents page displayed!")
    
    def test_document_page(self):
        PF.create_base_project()
        d = Document.objects.all()[0]
        self.selenium.get('%s/%s%i/' % (self.live_server_url, _('documents_url'), d.pk))
        time.sleep(SELENIUM_SLEEP_TIME + 2)
        try:
            self.selenium.find_element_by_xpath('//h3[contains(text(),"' + d.title + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Document page not displayed correctly!")
    
    def test_document_with_page_select_page(self):
        PF.create_base_project()
        d = Document.objects.all()[0]
        self.selenium.get('%s/%s%i/?page=2' % (self.live_server_url, _('documents_url'), d.pk))
        time.sleep(SELENIUM_SLEEP_TIME + 2)
        elem = self.selenium.find_element_by_xpath('//input[@id="page_num"]')
        self.assertEqual(elem.get_attribute('value'), '2', "Page on document page not selected/displayed correctly!")
    
    def test_search_page(self):
        PF.create_base_project()
        q = '1'
        self.selenium.get('%s/%s?q=%s' % (self.live_server_url, _('search_url'), q))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + q + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Search page not displayed correctly!")
    
    def test_contact_page(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('contact_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h2[contains(text(),"' + _('Contact') + '")]')
        except NoSuchElementException:
            self.assertTrue(0, "Contact page not displayed correctly!")
    
    
    
    
    