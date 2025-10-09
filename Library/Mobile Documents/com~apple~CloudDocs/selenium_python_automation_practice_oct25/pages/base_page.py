from seleniumpagefactory.Pagefactory import PageFactory
from utils.web_driver_setup import WebDriverSetUp
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class BasePage(WebDriverSetUp, PageFactory):
    def __init__(self, driver):
        self.driver = driver
        default_timeout = int(os.getenv("WD_WAIT", "10"))
        self.wait = WebDriverWait(self.driver, default_timeout)

    def wait_for_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
