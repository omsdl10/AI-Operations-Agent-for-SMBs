from app.core.config import settings


class ReminderMessageService:
    def follow_up_message(self, customer_name: str | None, title: str) -> str:
        return self._openai_message(
            "follow_up",
            f"Customer: {customer_name or 'Customer'}\nTask: {title}",
        ) or f"Follow up with {customer_name or 'this customer'} about: {title}."

    def payment_reminder_message(self, customer_name: str | None, invoice_number: str, amount: str) -> str:
        return self._openai_message(
            "payment_reminder",
            f"Customer: {customer_name or 'Customer'}\nInvoice: {invoice_number}\nAmount: {amount}",
        ) or f"Payment reminder for {customer_name or 'customer'}: invoice {invoice_number} for {amount} needs attention."

    def appointment_reminder_message(self, customer_name: str | None, title: str) -> str:
        return self._openai_message(
            "appointment_reminder",
            f"Customer: {customer_name or 'Customer'}\nAppointment: {title}",
        ) or f"Appointment reminder for {customer_name or 'customer'}: {title} is coming up soon."

    def _openai_message(self, reminder_type: str, context: str) -> str | None:
        if not settings.openai_api_key:
            return None
        for _attempt in range(2):
            try:
                from langchain_openai import ChatOpenAI

                model = ChatOpenAI(
                    model=settings.openai_model,
                    api_key=settings.openai_api_key,
                    temperature=0.2,
                )
                response = model.invoke(
                    [
                        (
                            "system",
                            "Write concise internal reminder text for a small business operations dashboard.",
                        ),
                        ("human", f"Reminder type: {reminder_type}\n{context}"),
                    ]
                )
                content = response.content if isinstance(response.content, str) else str(response.content)
                return content.strip()[:1000] or None
            except Exception:
                continue
        return None

