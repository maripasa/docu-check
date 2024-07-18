import datetime
import logging
from typing import Protocol

import lib.variables as var
from lib.email_tools import EmailServiceDocucheck
# Import functions/classes from custom modules
from lib.validate_tools import validate_cnpj
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tabulate import tabulate
from webdriver_manager.chrome import ChromeDriverManager

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


def filter_expired(table_data: list[dict]) -> list[dict]:
    """
    Filter the documents table to get only the expired documents.
    """
    logger.debug(f"Filtering expired documents from the table")
    expired_docs = [document for document in table_data if document["status"] == 'Vencido']

    logger.debug(f"filtered {table_data} into {expired_docs}")
    return expired_docs


def filter_near_expired(table_data: list[dict], days_remaining: int = 10) -> list[dict]:
    """
    Filter the documents table to get only the documents that will expire in the next 'days_remaining' days.
    """
    logger.debug(f"Filtering {days_remaining} left to expire documents from the table")
    dated_docs = [document for document in table_data if document["validade"] != '' and document['status'] != 'Vencido']
    today = datetime.date.today()
    near_expired_docs = [document for document in dated_docs if (
            datetime.datetime.strptime(document["validade"], '%d/%m/%Y').date() - today).days < days_remaining]

    logger.debug(f"filtered {table_data} into {near_expired_docs}")
    return near_expired_docs


class DocumentScrapper:

    def __init__(self, driver: WebDriver):

        self.driver = driver

    def get_documentation_info(self, receiver_cnpj: str) -> list[dict]:
        """
        Manages the process of collecting documentation information.
        """

        logger.info(f"Collecting documentation from CNPJ: {receiver_cnpj}")
        if not validate_cnpj(receiver_cnpj):
            raise InvalidCredentials("invalid CNPJ")

        table = self.collect_table_sefaz(driver=self.driver, receiver_cnpj=receiver_cnpj)
        table_data = self.scrape_table_sefaz(table=table[0], table_header=table[1])
        extracted_data = self.extract_required_info_sefaz(table_data)

        return extracted_data

    @staticmethod
    def collect_table_sefaz(driver, receiver_cnpj) -> tuple:
        """
        Access documentation information site from the UI.
        """
        try:
            logger.info("Collecting table data from SEFAZ")
            driver.get(var.url)
            driver.implicitly_wait(30)
            click_element(driver, var.juridic_person_button)
            input_text(driver, var.cnpj_input, receiver_cnpj)
            click_element(driver, var.consult_button, 2)

            # Gets the table rows
            table = driver.find_elements(By.XPATH, f"{var.comp_doc_table_body}//tr")
            # Gets the table headers
            table_header = driver.find_elements(By.XPATH, f"{var.comp_doc_table_subheader}//tr//th")

            logger.debug(f"Collected table {table} with headers {table_header}")
            return table, table_header
        except Exception as e:
            logger.critical(f"Error collecting table data from SEFAZ: {e}")
            driver.quit()
            raise

    @staticmethod
    def scrape_table_sefaz(table: list[dict], table_header: list) -> list[dict]:
        """
        Collect documentation information from the site.
        """
        table_data = []

        try:
            for document in table:
                document_values = {}
                for header, cell in zip(table_header, document.find_elements(By.XPATH, "td")):
                    header = header.text
                    cell = cell.text
                    document_values[header.lower()] = cell

                table_data.append(document_values)

            return table_data
        except Exception as e:
            logger.critical(f"Error scraping table data from SEFAZ: {e}")
            raise

    @staticmethod
    def extract_required_info_sefaz(data: list[dict]) -> list[dict]:
        logger.info("Extracting required information from table data")
        extracted_data = []
        for document in data:
            status = document['status']
            tipo = document['tipo']
            validade = document['validade']
            extracted_data.append({'status': status, 'tipo': tipo, 'validade': validade})

        logger.debug(f"Extracted data: {extracted_data}")
        return extracted_data


class EmailMessage:

    def __init__(self, expired_docs: list[dict], near_expired_docs: list[dict]) -> None:
        logger.info("Generating email message")

        table_expired = self.generate_table(expired_docs)
        table_near_expired = self.generate_table(near_expired_docs)
        self._message = self.generate_email_body(table_expired, table_near_expired)

    @property
    def message(self):
        return self._message

    @staticmethod
    def generate_table(table: list[dict]) -> str:
        """
        Generate a table with the given data.
        """
        logger.debug(f"Generating table with data: {table}")
        if not table:
            return ''

        table_data = [['Status', 'Tipo', 'Validade']]

        for document in table:
            table_data.append([document['status'], document['tipo'], document['validade']])

        formatted_table = tabulate(table_data, headers='firstrow', tablefmt='simple')

        logger.debug(f"Generated table: {formatted_table} with data: {table_data}")
        return formatted_table

    @staticmethod
    def generate_email_body(table_expired: str, table_near_expired: str, days_remaining: int = 10) -> str:
        """
        Generate the email body with the expired and near expired documents.
        """
        logger.debug(f"Generating email body with: {table_expired} and {table_near_expired}")

        message = ''

        if table_expired != '' or table_near_expired != '':
            message += (f"DocuCheck detectou os seguintes Documentos vencidos e/ou "
                        f"Documentos que vão vencer em {days_remaining} dias:\n\n")

        if table_expired != '':
            message += "Documentos Vencidos:\n"
            message += table_expired
            message += "\n"

        if table_near_expired != '':
            message += f"Documentos que vão vencer em {days_remaining} dias:\n"
            message += table_near_expired
            message += "\n"

        logger.debug(f"Generated email body: {message}")
        return message


class DocuCheck:
    def __init__(self, receiver_email, receiver_cnpj):
        self.receiver_email = receiver_email
        self.receiver_cnpj = receiver_cnpj

    def execute(self):
        """
        Execute the DocuCheck process.
        """
        logger.info("Executing DocuCheck")
        driver = None

        try:
            driver = initialize_chrome_driver()

            scrapper = DocumentScrapper(driver)
            data = scrapper.get_documentation_info(self.receiver_cnpj)

            driver.quit()
            driver = None

            expired_docs = filter_expired(data)
            near_expired_docs = filter_near_expired(data)

            email = EmailMessage(expired_docs, near_expired_docs)

            gmail_email_sender = EmailServiceDocucheck()

            gmail_email_sender.send_message(self.receiver_email,
                                            "DocuCheck - Documentos Vencidos e/ou Próximos do Vencimento",
                                            email.message)
        finally:
            if driver:
                driver.quit()
            logger.info("DocuCheck finished")
