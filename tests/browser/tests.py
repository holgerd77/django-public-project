from public_project.utils.test_utils import build_test_suite_from
from browser.generic_test import GenericTest
from browser.ui_elements_test import UIElementsTest
from browser.rss_test import RSSTest
from browser.api_test import APITest

test_cases = [
    GenericTest,
    UIElementsTest,
    RSSTest,
    APITest,
]

def suite():
    return build_test_suite_from(test_cases)
