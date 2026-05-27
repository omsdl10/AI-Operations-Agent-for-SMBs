INTENT_CLASSIFICATION_PROMPT = """
Classify the customer WhatsApp message for a small business operations agent.
Return one intent from the supported intent list and a confidence score from 0 to 1.
Supported intents: pricing_inquiry, sales_lead, support_request, appointment_booking,
payment_issue, follow_up_response, complaint, general_question, unknown.
"""

REPLY_GENERATION_PROMPT = """
Draft a concise, friendly WhatsApp reply for a small business.
Keep it helpful, specific to the intent, and avoid inventing unavailable details.
If the request requires staff approval, say the team will review and follow up shortly.
"""

