import imaplib
from email import message_from_bytes
from email.header import decode_header
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime
import pytz
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Message, EmailAccount

IMAP_SERVERS = {
    'gmail.com': 'imap.gmail.com',
    'yandex.ru': 'imap.yandex.ru',
    'mail.ru': 'imap.mail.ru',
}


def get_imap_server(email_account):
    domain = email_account.split('@')[-1]
    return IMAP_SERVERS.get(domain, None)


def fetch_emails(email, password, channel_name):
    try:

        if not isinstance(channel_name, str) or not channel_name:
            raise ValueError("Channel name must be a non-empty string.")

        imap_server = get_imap_server(email)
        if not imap_server:
            raise ValueError(f"IMAP server not found for domain {email.split('@')[-1]}")

        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email, password)
        mail.select('inbox')

        status, messages = mail.search(None, 'ALL')
        mail_ids = messages[0].split()

        email_account = EmailAccount.objects.get(email=email)

        total_emails = len(mail_ids)
        for index, mail_id in enumerate(mail_ids):
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            msg = message_from_bytes(msg_data[0][1])

            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            sent_date_str = msg["Date"]
            sent_date = None
            try:
                parsed_date = parsedate_tz(sent_date_str)
                if parsed_date:
                    sent_date = datetime.fromtimestamp(mktime_tz(parsed_date), pytz.UTC)
            except Exception as e:
                print(f"Error parsing date: {e}")

            body = ""

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode("utf-8")
                    except UnicodeDecodeError:
                        body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                elif part.get_content_type() == "text/html":
                    continue

            message_instance = Message.objects.create(
                email_account=email_account,
                subject=subject,
                sent_date=sent_date,
                received_date=None,
                body=body,
                attachments=[]
            )

            progress = (index + 1) / total_emails * 100
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(
                channel_name,
                {
                    "type": "progress_update",
                    "progress": int(progress),
                    "message": {
                        "subject": subject,
                        "sent_date": sent_date.isoformat() if sent_date else None,
                        "body": body
                    }
                }
            )

    except Exception as e:
        print(f"Error fetching emails: {e}")
