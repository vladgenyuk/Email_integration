import os
import email.header

from datetime import datetime
from imapclient import IMAPClient
from email import message_from_bytes
from email.utils import parsedate_to_datetime

from email_integration.settings.config import EMAIL_STATUS

class ImapManager:
    def __init__(self):
        self.now = datetime.now().strftime("%Y%m%d%H%M%S")
        self.now_valid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def decode_subject(self, subject_encoded):
        decoded_fragments = email.header.decode_header(subject_encoded)
        subject = ''

        for fragment, encoding in decoded_fragments:
            if isinstance(fragment, bytes):
                try:
                    if encoding is None:
                        subject += fragment.decode('utf-8', errors='replace')
                    else:
                        subject += fragment.decode(encoding, errors='replace')
                except LookupError:
                    subject += fragment.decode('utf-8', errors='replace')
            else:
                subject += fragment

        return subject

    def save_attachment(self, msg, download_folder="email_attachments"):
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        attachments = []

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                filename = email.header.decode_header(filename)[0][0]
                if isinstance(filename, bytes):
                    filename = filename.decode()
                filename = self.now + filename

                filepath = os.path.join(download_folder, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))

                attachments.append(filename)
        return attachments

    def get_email_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True)
                    return body.decode(part.get_content_charset() or 'utf-8')
        else:
            body = msg.get_payload(decode=True)
            return body.decode(msg.get_content_charset() or 'utf-8')

        return ''

    def fetch_emails(self, email_provider: str = 'imap.yandex.ru',
                     email_login: str = 'genyukvlad@yandex.ru',
                     email_password: str = 'ibhubfgalimremne',
                     email_status: str = EMAIL_STATUS,
                     email_folder: str = 'INBOX',
                     ):
        with IMAPClient(email_provider, port=993) as client:
            client.login(email_login, email_password)  # Оставил свою тестовую почту и пароль
            client.select_folder(email_folder)
            messages = client.search(email_status)
            messages_count = len(messages)

            for msgid, data in client.fetch(messages, 'RFC822').items():
                msg = message_from_bytes(data[b'RFC822'])
                subject = msg['subject']
                from_email = msg['from']
                to_email = msg['to']
                body = self.get_email_body(msg)
                sent_at = msg['Date']
                sent_at = parsedate_to_datetime(sent_at) if sent_at else None
                attachments = self.save_attachment(msg)

                yield {
                    'subject': self.decode_subject(subject),
                    'from_email': self.decode_subject(from_email),
                    'to_email': self.decode_subject(to_email),
                    'body': body or '',
                    'messages_count': messages_count,
                    'attachments': attachments,
                    'sent_at': sent_at,
                    'received_at': self.now_valid,
                    'email_provider': email_provider
                }
