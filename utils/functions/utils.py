import logging
from typing import Protocol

from selenium.webdriver.common.by import By

logger = logging.getLogger("docucheck.core")


class InvalidCredentials(Exception):
    pass


class WebDriver(Protocol):
    def find_element(self, by: str, value: str) -> any:
        ...

    def find_elements(self, by: str, value: str) -> any:
        ...

    def click(self) -> None:
        ...

    def send_keys(self, text: str) -> None:
        ...


class EmailSender(Protocol):
    def send_message(self, to_email: str, subject: str, body: str) -> None:
        ...


def click_element(driver: WebDriver, xpath: str, times: int = 1) -> None:
    """
    Click the element located by the given xpath.
    """
    logger.debug(f"Clicking element with xpath: {xpath} {times} times")

    element = driver.find_element(By.XPATH, xpath)
    for _ in range(times):
        element.click()


def input_text(driver: WebDriver, xpath: str, text: str) -> None:
    """
    Input text into the element located by the given xpath.
    """
    logger.debug(f"Inputting text: {text} into element with xpath: {xpath}")
    element = driver.find_element(By.XPATH, xpath)
    click_element(driver, xpath)
    element.send_keys(text)
