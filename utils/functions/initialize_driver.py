import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("docucheck.core")


def initialize_chrome_driver() -> webdriver.Chrome:
    """
    Initialize a Chrome WebDriver instance with specified options.
    """
    logger.info("initializing Chrome WebDriver")

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    driver_path = ChromeDriverManager().install()

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)

    logger.info(f"Chrome WebDriver initialized successfully")
    logger.debug(f"CWD path: {driver_path}; Driver: {driver}")
    return driver
