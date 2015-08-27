import time, unittest
from django.test import LiveServerTestCase
from django.utils.translation import ugettext as _  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from fixtures.project_factory import ProjectFactory as PF
from public_project.models import *


SELENIUM_SLEEP_TIME = 2


class UIElementsTest(LiveServerTestCase):
    """
    Tests for specific UI elements realized with jQuery/Javascript
    """
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(UIElementsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UIElementsTest, cls).tearDownClass()
    
    @unittest.skip("Test is unreliable - eventually some timing issue - no solution found yet")
    def test_search_box_autocomplete_universal_search(self):
        PF.create_base_project()
        self.selenium.get('%s/' % (self.live_server_url))
        elem = self.selenium.find_element_by_xpath('//input[@id="q"]')
        elem.send_keys("Tes")
        time.sleep(1)
        elem.send_keys("t")
        time.sleep(SELENIUM_SLEEP_TIME)
        elem.send_keys(Keys.RETURN)
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//div[@id="info_box_participants"]')
        except NoSuchElementException:
            self.assertTrue(0, "No search page with participant(s) displayed!")
    
    def test_search_box_autocomplete_navigate(self):
        PF.create_base_project()
        self.selenium.get('%s/' % (self.live_server_url))
        elem = self.selenium.find_element_by_xpath('//input[@id="q"]')
        elem.send_keys("Tes")
        time.sleep(1)
        elem.send_keys("t")
        time.sleep(1)
        elem.send_keys(Keys.ARROW_DOWN)
        time.sleep(SELENIUM_SLEEP_TIME)
        elem.send_keys(Keys.RETURN)
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//h3[contains(text(),"Test Corporation")]')
        except NoSuchElementException:
            self.assertTrue(0, "No participant detail page displayed!")
    
    def test_expand_collapse(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('participants_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        self.selenium.find_element_by_xpath('//button[@id="bg_expand"]').click()
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//div[@id="pt_ec_box_1" and contains(@style,"display: block")]')
        except NoSuchElementException:
            self.assertTrue(0, "Expand/collapse UI element not working!")
    
    def test_events_topic_selector(self):
        PF.create_base_project()
        self.selenium.get('%s/%s' % (self.live_server_url, _('events_url')))
        time.sleep(SELENIUM_SLEEP_TIME)
        elem = self.selenium.find_element_by_xpath('//select[@id="mpp_events_select"]')
        elem.click()
        time.sleep(1)
        elem.send_keys(Keys.ARROW_DOWN)
        time.sleep(SELENIUM_SLEEP_TIME)
        elem.send_keys(Keys.RETURN)
        time.sleep(SELENIUM_SLEEP_TIME)
        try:
            self.selenium.find_element_by_xpath('//div[@id="events_4" and contains(@style,"display: block")]//a[contains(text(),"2")]')
        except NoSuchElementException:
            self.assertTrue(0, "Events topic selector not working!")
        
