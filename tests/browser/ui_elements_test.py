import time
from django.test import LiveServerTestCase
from django.utils.translation import ugettext as _  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from fixtures.project_factory import ProjectFactory as PF
from public_project.models import *


SELENIUM_SLEEP_TIME = 3


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
