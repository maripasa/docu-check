import logging

from selenium.webdriver.common.by import By

from utils.functions.utils import click_element, input_text, InvalidCredentials, WebDriver
from utils.functions.validate_tools import validate_cnpj
from utils.variables import fornecedor_web_variables as var

logger = logging.getLogger("docucheck.core")


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
