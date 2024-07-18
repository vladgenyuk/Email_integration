import json
import asyncio
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import ImapManager
from .models import EmailMessage


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("email_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("email_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data.get('user_id')
        imap_manager = ImapManager()
        emails = imap_manager.fetch_emails(
            email_provider=data.get('email_provider'),
            email_login=data.get('email_login'),
            email_password=data.get('email_password')
        )
        for email in emails:
            # await asyncio.sleep(0.5)
            await self.send(text_data=json.dumps(
                [
                    'progress_bar',
                    {
                        'messages_count': email.get('messages_count'),
                        'add': 1,
                    }
                ]
            ))
            await sync_to_async(EmailMessage.objects.create)(
                subject=email.get('subject'),
                from_email=email.get('from_email'),
                to_email=email.get('to_email'),
                attachments=email.get('attachments'),
                received_at=email.get('received_at'),
                sent_at=email.get('sent_at'),
                body=email.get('body'),
                user_id=user_id,
                email_service=email.get('email_provider')
            )
