"""
Esse programa é totalmente gambiarra até ser refatorado.
"""
import smtplib

# gambiarra
import os
import json

from email.message import EmailMessage


class EmailServiceDocucheck:
    def __init__(self) -> None:
        # gambiarra
        credentials_filepath = os.path.join("docucheck", "data", "credentials.json")
        with open(credentials_filepath) as file:
            credentials = json.load(file)
        self.smtp_server = 'smtp.gmail.com'
        self.port = 587
        self.sender_email = credentials['email']
        self.sender_password = credentials['password']

    def send_message(self, to_email: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['To'] = to_email
        msg.set_content(body)

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.sender_email, self.sender_password, initial_response_ok=True)
        server.send_message(msg)

        server.quit()


"""class EmailSender:
    def __init__(self, smtp_server: str, port: int, email: str, password: str) -> None:
        self.smtp_server = smtp_server
        self.port = port
        self.email = email
        self.password = password

    def send_message(self, to_email: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['To'] = to_email
        msg.set_content(body)

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.sender_email, self.sender_password, initial_response_ok=True)
        server.send_message(msg)

        server.quit()  """
