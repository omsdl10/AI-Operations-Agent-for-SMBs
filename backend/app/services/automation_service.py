from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.ai_log import AILog, AILogStatus
from app.models.appointment import Appointment, AppointmentStatus
from app.models.business import Business
from app.models.follow_up import FollowUp, FollowUpStatus
from app.models.invoice import Invoice, InvoiceStatus
from app.models.notification import Notification, NotificationStatus
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import AutomationRunResult
from app.services.reminder_message_service import ReminderMessageService


@dataclass
class AutomationCounters:
    follow_up_notifications: int = 0
    payment_reminders: int = 0
    appointment_reminders: int = 0
    overdue_invoices: int = 0

    @property
    def total_notifications(self) -> int:
        return self.follow_up_notifications + self.payment_reminders + self.appointment_reminders


class AutomationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.notifications = NotificationRepository(db)
        self.message_generator = ReminderMessageService()

    def run_due_automations(self) -> AutomationRunResult:
        counters = AutomationCounters()
        now = datetime.utcnow()

        counters.overdue_invoices = self.detect_overdue_invoices(now)
        counters.follow_up_notifications = self.schedule_due_follow_up_notifications(now)
        counters.payment_reminders = self.schedule_payment_reminders(now)
        counters.appointment_reminders = self.schedule_appointment_reminders(now)
        self.mark_due_notifications_sent(now)
        self.log_job("run_due_automations", counters)

        self.db.commit()
        return AutomationRunResult(
            follow_up_notifications=counters.follow_up_notifications,
            payment_reminders=counters.payment_reminders,
            appointment_reminders=counters.appointment_reminders,
            overdue_invoices=counters.overdue_invoices,
            total_notifications=counters.total_notifications,
        )

    def detect_overdue_invoices(self, now: datetime) -> int:
        invoices = list(
            self.db.scalars(
                select(Invoice)
                .options(selectinload(Invoice.customer))
                .where(
                    Invoice.due_at.is_not(None),
                    Invoice.due_at < now,
                    Invoice.status == InvoiceStatus.sent.value,
                )
            ).all()
        )
        for invoice in invoices:
            invoice.status = InvoiceStatus.overdue.value
        return len(invoices)

    def schedule_due_follow_up_notifications(self, now: datetime) -> int:
        follow_ups = list(
            self.db.scalars(
                select(FollowUp)
                .options(selectinload(FollowUp.customer))
                .where(
                    FollowUp.due_at <= now,
                    FollowUp.status.in_([FollowUpStatus.pending.value, FollowUpStatus.scheduled.value]),
                )
            ).all()
        )
        created = 0
        for follow_up in follow_ups:
            follow_up.status = FollowUpStatus.overdue.value
            if self.notifications.exists_for_reference(follow_up.business_id, "follow_up_id", follow_up.id):
                continue
            self.notifications.create(
                Notification(
                    business_id=follow_up.business_id,
                    user_id=follow_up.assigned_user_id,
                    title="Follow-up due",
                    body=self.message_generator.follow_up_message(
                        follow_up.customer.full_name if follow_up.customer else None,
                        follow_up.title,
                    ),
                    channel="in_app",
                    status=NotificationStatus.pending.value,
                    scheduled_for=now,
                    metadata_json={"follow_up_id": follow_up.id, "automation": "scheduled_follow_up"},
                )
            )
            created += 1
        return created

    def schedule_payment_reminders(self, now: datetime) -> int:
        invoices = list(
            self.db.scalars(
                select(Invoice)
                .options(selectinload(Invoice.customer))
                .where(
                    Invoice.status == InvoiceStatus.overdue.value,
                    Invoice.customer_id.is_not(None),
                )
            ).all()
        )
        created = 0
        for invoice in invoices:
            if self.notifications.exists_for_reference(invoice.business_id, "invoice_id", invoice.id):
                continue
            amount = f"{invoice.currency} {invoice.amount_cents / 100:,.2f}"
            self.notifications.create(
                Notification(
                    business_id=invoice.business_id,
                    title="Payment reminder",
                    body=self.message_generator.payment_reminder_message(
                        invoice.customer.full_name if invoice.customer else None,
                        invoice.invoice_number,
                        amount,
                    ),
                    channel="in_app",
                    status=NotificationStatus.pending.value,
                    scheduled_for=now + timedelta(minutes=5),
                    metadata_json={"invoice_id": invoice.id, "automation": "payment_reminder"},
                )
            )
            created += 1
        return created

    def schedule_appointment_reminders(self, now: datetime) -> int:
        window_end = now + timedelta(hours=24)
        appointments = list(
            self.db.scalars(
                select(Appointment)
                .options(selectinload(Appointment.customer))
                .where(
                    Appointment.starts_at >= now,
                    Appointment.starts_at <= window_end,
                    Appointment.status.in_(
                        [AppointmentStatus.scheduled.value, AppointmentStatus.confirmed.value]
                    ),
                )
            ).all()
        )
        created = 0
        for appointment in appointments:
            if self.notifications.exists_for_reference(
                appointment.business_id,
                "appointment_id",
                appointment.id,
            ):
                continue
            self.notifications.create(
                Notification(
                    business_id=appointment.business_id,
                    title="Appointment reminder",
                    body=self.message_generator.appointment_reminder_message(
                        appointment.customer.full_name if appointment.customer else None,
                        appointment.title,
                    ),
                    channel="in_app",
                    status=NotificationStatus.pending.value,
                    scheduled_for=max(now, appointment.starts_at - timedelta(hours=2)),
                    metadata_json={"appointment_id": appointment.id, "automation": "appointment_reminder"},
                )
            )
            created += 1
        return created

    def mark_due_notifications_sent(self, now: datetime) -> None:
        for notification in self.notifications.due_pending(now):
            notification.status = NotificationStatus.sent.value
            notification.sent_at = now

    def log_job(self, job_name: str, counters: AutomationCounters) -> None:
        business_ids = list(self.db.scalars(select(Business.id)).all())
        for business_id in business_ids:
            self.db.add(
                AILog(
                    business_id=business_id,
                    workflow_name="automation_worker",
                    node_name=job_name,
                    status=AILogStatus.success.value,
                    input_payload={},
                    output_payload={
                        "follow_up_notifications": counters.follow_up_notifications,
                        "payment_reminders": counters.payment_reminders,
                        "appointment_reminders": counters.appointment_reminders,
                        "overdue_invoices": counters.overdue_invoices,
                        "total_notifications": counters.total_notifications,
                    },
                    reasoning="Automation worker completed scheduled checks.",
                )
            )
