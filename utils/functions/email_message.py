import logging

from tabulate import tabulate

logger = logging.getLogger("docucheck.core")


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
