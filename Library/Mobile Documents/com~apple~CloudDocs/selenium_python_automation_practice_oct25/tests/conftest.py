import os
import pytest
import allure
from utils.web_driver_setup import create_driver, quit_driver
from pages.login import LoginPage
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os.path

# Ensure screenshot directory exists
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.fixture(scope="function")
def driver():
    opts = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
    d = create_driver(options=opts)
    d.implicitly_wait(2)
    yield d
    quit_driver(d)


# legacy per-page fixtures removed in favor of the `pages` container


class Pages:
    """Container for page objects. Lazily instantiates pages when accessed.

    Usage in tests:
        def test_something(pages):
            pages.login.open(url)
    """

    def __init__(self, driver):
        self._driver = driver
        self._instances = {}

    def login(self):
        # explicit factory method for LoginPage
        if 'login' not in self._instances:
            self._instances['login'] = LoginPage(self._driver)
        return self._instances['login']


@pytest.fixture(scope="function")
def pages(driver):
    return Pages(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure."""
    outcome = yield
    result = outcome.get_result()

    # Check if the test failed during the call phase
    if result.when == "call" and result.failed:
        # Get the driver from pages, login_page or driver fixture
        driver = None
        if "pages" in item.fixturenames:
            pages_obj = item.funcargs.get("pages")
            driver = getattr(pages_obj, '_driver', None)
        elif "login_page" in item.fixturenames:
            login_page = item.funcargs.get("login_page")
            driver = login_page.driver
        elif "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")

        if driver:
            # Generate a unique filename with timestamp and test name
            test_name = item.name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(
                SCREENSHOT_DIR, f"failure_{test_name}_{timestamp}.png")
            try:
                driver.get_screenshot_as_file(screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
                # Attach screenshot to Allure report
                if os.path.exists(screenshot_path):
                    with open(screenshot_path, "rb") as f:
                        allure.attach(f.read(
                        ), name=f"screenshot-{test_name}", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")

            # Attach traceback or longrepr if available
            if hasattr(result, "longrepr") and result.longrepr:
                try:
                    allure.attach(str(result.longrepr), name="traceback",
                                  attachment_type=allure.attachment_type.TEXT)
                except Exception:
                    pass
