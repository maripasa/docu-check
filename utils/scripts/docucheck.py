import logging

from utils.functions.email_message import EmailMessage
from utils.functions.filter import filter_expired, filter_near_expired
from utils.functions.initialize_driver import initialize_chrome_driver
from utils.scripts.document_scrapper import DocumentScrapper
from utils.scripts.email_tools import EmailServiceDocucheck

logger = logging.getLogger("docucheck.core")


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
