import datetime
import logging

logger = logging.getLogger("docucheck.core")


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
