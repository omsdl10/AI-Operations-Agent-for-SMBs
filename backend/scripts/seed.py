from datetime import date, datetime, timedelta
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.db.session import SessionLocal
from app.models import (
    AILog,
    Appointment,
    AppointmentStatus,
    Business,
    Customer,
    DailySummary,
    FollowUp,
    FollowUpStatus,
    Invoice,
    InvoiceStatus,
    Lead,
    LeadStatus,
    Message,
    MessageChannel,
    MessageDirection,
    MessageStatus,
    Notification,
    NotificationStatus,
    User,
    UserRole,
)
from app.repositories.user_repository import UserRepository
from app.services.security import hash_password

SEED_EMAIL = "owner@example.com"
SEED_PASSWORD = "password123"


def seed() -> None:
    db = SessionLocal()
    try:
        if UserRepository(db).get_by_email(SEED_EMAIL):
            print("Seed data already exists.")
            return

        business = Business(
            name="Bright Smile Dental",
            phone="+15551234567",
            industry="Dental Clinic",
        )
        db.add(business)
        db.flush()

        owner = User(
            business_id=business.id,
            email=SEED_EMAIL,
            full_name="Avery Patel",
            hashed_password=hash_password(SEED_PASSWORD),
            role=UserRole.owner.value,
        )
        db.add(owner)

        customer = Customer(
            business_id=business.id,
            full_name="Maya Johnson",
            phone="+15557654321",
            email="maya@example.com",
            notes="Interested in whitening and regular cleaning.",
            tags=["vip", "whatsapp"],
        )
        db.add(customer)
        db.flush()

        lead = Lead(
            business_id=business.id,
            customer_id=customer.id,
            title="Teeth whitening package",
            status=LeadStatus.interested.value,
            source="whatsapp",
            value_cents=29900,
            priority_score=82,
            notes="Asked about pricing and next available appointment.",
        )
        db.add(lead)
        db.flush()

        message = Message(
            business_id=business.id,
            customer_id=customer.id,
            direction=MessageDirection.inbound.value,
            channel=MessageChannel.whatsapp.value,
            status=MessageStatus.received.value,
            body="Hi, what is the price for teeth whitening?",
            external_id="SM_seed_001",
        )
        db.add(message)
        db.flush()

        invoice = Invoice(
            business_id=business.id,
            customer_id=customer.id,
            invoice_number="INV-1001",
            status=InvoiceStatus.sent.value,
            amount_cents=29900,
            currency="USD",
            due_at=datetime.utcnow() + timedelta(days=7),
        )
        db.add(invoice)

        appointment = Appointment(
            business_id=business.id,
            customer_id=customer.id,
            title="Whitening consultation",
            status=AppointmentStatus.scheduled.value,
            starts_at=datetime.utcnow() + timedelta(days=1, hours=2),
            ends_at=datetime.utcnow() + timedelta(days=1, hours=3),
            location="Room 2",
        )
        db.add(appointment)
        db.flush()

        follow_up = FollowUp(
            business_id=business.id,
            customer_id=customer.id,
            lead_id=lead.id,
            assigned_user_id=owner.id,
            status=FollowUpStatus.scheduled.value,
            title="Send whitening prep details",
            notes="Follow up if Maya does not confirm by tomorrow morning.",
            due_at=datetime.utcnow() + timedelta(hours=18),
        )
        db.add(follow_up)

        summary = DailySummary(
            business_id=business.id,
            summary_date=date.today(),
            content="One new qualified lead came from WhatsApp. One consultation was scheduled.",
            metrics={
                "new_leads": 1,
                "conversations_handled": 1,
                "pending_follow_ups": 1,
                "appointments_today": 0,
            },
            recommendations=[
                "Confirm Maya's appointment details by WhatsApp.",
                "Offer a bundle with routine cleaning.",
            ],
        )
        db.add(summary)

        ai_log = AILog(
            business_id=business.id,
            user_id=owner.id,
            customer_id=customer.id,
            lead_id=lead.id,
            message_id=message.id,
            appointment_id=appointment.id,
            workflow_name="customer_message_agent",
            node_name="classify_intent_node",
            input_payload={"message_text": message.body},
            output_payload={"intent": "pricing_inquiry", "confidence_score": 0.91},
            reasoning="Seeded example of a pricing inquiry classification.",
        )
        db.add(ai_log)

        notification = Notification(
            business_id=business.id,
            user_id=owner.id,
            title="Follow-up scheduled",
            body="Maya Johnson needs a whitening consultation follow-up.",
            status=NotificationStatus.pending.value,
            scheduled_for=datetime.utcnow() + timedelta(hours=18),
            metadata_json={"follow_up_id": follow_up.id},
        )
        db.add(notification)

        db.commit()
        print(f"Seed data created. Login with {SEED_EMAIL} / {SEED_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

