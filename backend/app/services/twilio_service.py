from datetime import datetime

from fastapi import status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppException
from app.models.customer import Customer
from app.models.message import Message, MessageChannel, MessageDirection, MessageStatus
from app.repositories.message_repository import MessageRepository
from app.schemas.message import ConversationRead, MessageRead


class TwilioService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.messages = MessageRepository(db)

    def normalize_whatsapp_phone(self, value: str | None) -> str:
        if not value:
            return ""
        return value.replace("whatsapp:", "").strip()

    def resolve_webhook_business_id(self) -> str:
        if settings.twilio_default_business_id:
            return settings.twilio_default_business_id
        business_id = self.messages.get_default_business_id()
        if not business_id:
            raise AppException(
                "No business exists for inbound webhook handling.",
                status.HTTP_400_BAD_REQUEST,
                "business_not_configured",
            )
        return business_id

    def store_inbound_message(
        self,
        from_number: str,
        body: str,
        external_id: str | None,
        business_id: str | None = None,
    ) -> MessageRead:
        normalized_phone = self.normalize_whatsapp_phone(from_number)
        resolved_business_id = business_id or self.resolve_webhook_business_id()

        if external_id and self.messages.get_by_external_id(external_id):
            existing = self.messages.get_by_external_id(external_id)
            return MessageRead.model_validate(existing)

        customer = self.messages.get_customer_by_phone(resolved_business_id, normalized_phone)
        if not customer:
            customer = Customer(
                business_id=resolved_business_id,
                full_name=normalized_phone or "WhatsApp customer",
                phone=normalized_phone,
                tags=["whatsapp"],
            )
            self.db.add(customer)
            self.db.flush()

        message = self.messages.create(
            Message(
                business_id=resolved_business_id,
                customer_id=customer.id,
                direction=MessageDirection.inbound.value,
                channel=MessageChannel.whatsapp.value,
                status=MessageStatus.received.value,
                body=body,
                external_id=external_id,
            )
        )
        self.db.commit()
        return MessageRead.model_validate(message)

    def send_whatsapp_message(self, business_id: str, customer_id: str, body: str) -> MessageRead:
        customer = self.messages.get_customer(business_id, customer_id)
        if not customer or not customer.phone:
            raise AppException(
                "Customer has no WhatsApp-capable phone number.",
                status.HTTP_400_BAD_REQUEST,
                "customer_phone_missing",
            )

        external_id = None
        message_status = MessageStatus.sent.value

        if settings.twilio_mock_mode:
            external_id = f"mock_{int(datetime.utcnow().timestamp())}"
        else:
            external_id = self._send_via_twilio(customer.phone, body)

        message = self.messages.create(
            Message(
                business_id=business_id,
                customer_id=customer.id,
                direction=MessageDirection.outbound.value,
                channel=MessageChannel.whatsapp.value,
                status=message_status,
                body=body,
                external_id=external_id,
                sent_at=datetime.utcnow(),
            )
        )
        self.db.commit()
        return MessageRead.model_validate(message)

    def list_conversations(self, business_id: str) -> list[ConversationRead]:
        recent_messages = self.messages.list_recent_by_business(business_id)
        seen: set[str] = set()
        conversations: list[ConversationRead] = []

        for message in recent_messages:
            if not message.customer_id or message.customer_id in seen:
                continue
            seen.add(message.customer_id)
            conversations.append(
                ConversationRead(
                    customer_id=message.customer_id,
                    customer_name=message.customer.full_name if message.customer else "Unknown customer",
                    phone=message.customer.phone if message.customer else None,
                    last_message=message.body,
                    last_message_at=message.created_at,
                    unread_count=self.messages.count_unread_for_customer(business_id, message.customer_id),
                    status=message.status,
                )
            )
        return conversations

    def list_conversation_messages(self, business_id: str, customer_id: str) -> list[MessageRead]:
        customer = self.messages.get_customer(business_id, customer_id)
        if not customer:
            raise AppException("Customer not found.", status.HTTP_404_NOT_FOUND, "customer_not_found")
        return [
            MessageRead.model_validate(message)
            for message in self.messages.list_for_customer(business_id, customer_id)
        ]

    def update_message_status(self, external_id: str | None, message_status: str | None) -> bool:
        if not external_id or not message_status:
            return False

        message = self.messages.get_by_external_id(external_id)
        if not message:
            return False

        message.status = message_status
        self.db.commit()
        return True

    def _send_via_twilio(self, to_number: str, body: str) -> str:
        if not settings.twilio_account_sid or not settings.twilio_auth_token or not settings.twilio_whatsapp_from:
            raise AppException(
                "Twilio credentials are not configured.",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "twilio_not_configured",
            )

        from twilio.rest import Client

        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        response = client.messages.create(
            from_=settings.twilio_whatsapp_from,
            to=f"whatsapp:{to_number}",
            body=body,
        )
        return response.sid

