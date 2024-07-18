import logging

from utils.scripts.docucheck import DocuCheck

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("docucheck")

    receiver_email = "receiver@example.com"
    receiver_cnpj = "12345678000195"

    docucheck = DocuCheck(receiver_email, receiver_cnpj)
    docucheck.execute()
