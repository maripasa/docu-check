import logging
from typing import Protocol
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime

# Import functions/classes from custom modules
from lib.validate_tools import validate_email, validate_cnpj
from lib.email_tools import EmailService_Docucheck
import lib.variables as var

logger = logging.getLogger(__name__)

class InvalidCredentials(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.when = datetime.now()
        
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


def initialize_Chrome_driver() -> webdriver.Chrome:
    """
    Initialize a Chrome WebDriver instance with specified options.
    """
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

    logger
    return driver
  
def click_element(driver: WebDriver, xpath: str, times: int = 1) -> None:
    """
    Click the element located by the given xpath.
    """
    element = driver.find_element(By.XPATH, xpath)
    for x in range(times):
        element.click()

def input_text(driver: WebDriver, xpath: str, text: str) -> None:
    """
    Input text into the element located by the given xpath.
    """
    element = driver.find_element(By.XPATH, xpath)
    click_element(driver, xpath)
    element.send_keys(text)

def filter_expired(table_data: list[dict]) -> list[dict]:
    """
    Filter the documents table to get only the expired documents.
    """
    expired_docs = [document for document in table_data if document["status"] == 'Vencido']

    return expired_docs

def filter_near_expired(table_data: list[dict], days_remaining: int = 10) -> list[dict]:
    """
    Filter the documents table to get only the documents that will expire in the next 'days_remaining' days.
    """
    dated_docs = [document for document in table_data if document["validade"] != '']
    today = datetime.date.today()
    near_expired_docs = [document for document in dated_docs if (datetime.datetime.strptime(document["validade"], '%d/%m/%Y').date() - today).days < days_remaining]

    return near_expired_docs

class DocumentScrapper:
    
    def __init__(self, driver: WebDriver):
        
        self.driver = driver
    
    def get_documentation_info(self, receiver_cnpj: str) -> list[dict]:
        if not validate_cnpj(receiver_cnpj):
            raise InvalidCredentials("invalid CNPJ")
        
        table = self.collect_table_sefaz(driver=self.driver, receiver_cnpj=receiver_cnpj)
        table_data = self.scrape_table_sefaz(*table)
        extracted_data = self.extract_required_info_sefaz(table_data)
        
        return extracted_data
    
    def collect_table_sefaz(self, driver, receiver_cnpj) -> tuple:
        """
        Access documentation information site from the UI.
        """
        driver.get(var.url)
        driver.implicitly_wait(30)
        click_element(driver, var.juridic_person_button)
        input_text(driver, var.cnpj_input, receiver_cnpj)
        click_element(driver, var.consult_button, 2)

        # Gets the table rows
        table = driver.find_elements(By.XPATH, f"{var.comp_doc_table_body}//tr")
        # Gets the table headers
        table_header = driver.find_elements(By.XPATH, f"{var.comp_doc_table_subheader}//tr//th")
        
        return table, table_header

    def scrape_table_sefaz(self, *args) -> list[dict]:
        """
        Collect documentation information from the site.
        """
        table, table_header = args
        table_data = []

        for document in table:
            document_values = {}
            for header, cell in zip(table_header, document.find_elements(By.XPATH, "td")):
                header = header.text
                cell = cell.text
                document_values[header.lower()] = cell
                
            table_data.append(document_values)

        return table_data

    def extract_required_info_sefaz(self, data: list[dict]) -> list[dict]:
        extracted_data = []
        for document in data:
            status = document['status']
            tipo = document['tipo']
            validade = document['validade']
            extracted_data.append({'status': status, 'tipo': tipo, 'validade': validade})

        return extracted_data

class EmailMessage:
    
    def __init__(self, expired_docs: list[dict], near_expired_docs: list[dict]) -> None:
        
        table_expired = self.generate_table(expired_docs)
        table_near_expired = self.generate_table(near_expired_docs)
        self._message = self.generate_email_body(table_expired, table_near_expired)
    
    @property
    def message(self):
        return self._message
          
    def generate_table(self, table: list[dict]) -> str:
        """
        Generate a table with the given data.
        """
        if table == []:
            return ''

        table_data = [['Status', 'Tipo', 'Validade']]

        for document in table:
            table_data.append([document['status'], document['tipo'], document['validade']])

        return tabulate(table_data, headers='firstrow', tablefmt='rounded_outline')
        
    def generate_email_body(self, table_expired: str, table_near_expired: str, days_remaining: int = 10) -> str:
        """
        Generate the email body with the expired and near expired documents.
        """
        if table_expired == '' and table_near_expired == '':
            return ''
        message = f"DocuCheck detectou os seguintes Documentos vencidos e/ou Documentos que vão vencer em {days_remaining} dias:\n\n"

        if table_expired != '':
            message += "Documentos Vencidos:\n"
            message += table_expired
            message += "\n"

        if table_near_expired != '':
            message += f"Documentos que vão vencer em {days_remaining} dias:\n"
            message += table_near_expired
            message += "\n"

        return message

class DocuCheck:
    def __init__(self, receiver_email, receiver_cnpj):
        self.receiver_email = receiver_email
        self.receiver_cnpj = receiver_cnpj

    def execute(self):
        driver = initialize_Chrome_driver()
        try:
            scrapper = DocumentScrapper(driver)
            data = scrapper.get_documentation_info(self.receiver_cnpj)

            expired_docs = filter_expired(data)
            near_expired_docs = filter_near_expired(data)

            email = EmailMessage(expired_docs, near_expired_docs)

            GmailEmailSender = EmailService_Docucheck()

            GmailEmailSender.send_message(self.receiver_email,
                                          "DocuCheck - Documentos Vencidos e/ou Próximos do Vencimento",
                                          email.message)
        finally:
            driver.quit()