import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverSetUp:
    """Reusable driver helper class for tests (works with unittest or pytest).

    Usage:
      - In unittest: inherit and call super().set_up() / super().tear_down() in setUp/tearDown
      - In pytest fixtures: instantiate and call init_driver()/shutdown_driver()
    """

    def init_driver(self, options: Options | None = None):
        options = options or Options()
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        self.driver = create_driver(options=options)
        # short implicit wait to handle very fast lookups; prefer explicit waits via self.wait
        self.driver.implicitly_wait(2)
        # explicit wait utility available to tests/pages
        default_timeout = int(os.getenv("WD_WAIT", "10"))
        self.wait = WebDriverWait(self.driver, default_timeout)

    def shutdown_driver(self):
        if getattr(self, 'driver', None):
            quit_driver(self.driver)

    # Convenience wait helpers that accept locator tuples e.g. (By.ID, 'username')
    def wait_for_presence(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.wait._timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_visible(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.wait._timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.wait._timeout).until(
            EC.element_to_be_clickable(locator)
        )


def create_driver(options: Options | None = None):
    """Create and return a configured Chrome WebDriver instance."""
    opts = options or Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
    opts.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver


def quit_driver(driver):
    try:
        driver.quit()
    except Exception:
        pass


# module provides helpers for both unittest and pytest usage
