# Stage 8 LangGraph AI Agent

Stage 8 adds the customer message AI agent workflow.

Workflow nodes:

1. `receive_message_node`
2. `classify_intent_node`
3. `customer_lookup_node`
4. `ai_response_generation_node`
5. `action_decision_node`
6. `follow_up_creation_node`
7. `payment_reminder_node`
8. `appointment_scheduler_node`
9. `human_review_node`
10. `send_reply_node`
11. `log_activity_node`

Supported intents:

- `pricing_inquiry`
- `sales_lead`
- `support_request`
- `appointment_booking`
- `payment_issue`
- `follow_up_response`
- `complaint`
- `general_question`
- `unknown`

Rules implemented:

- Low confidence messages require human review.
- Complaint and unknown intents require human review.
- Payment-related messages look for open invoices.
- Appointment-related messages create a placeholder appointment for staff confirmation.
- Lead and pricing messages create CRM lead records.
- Follow-up-worthy messages create follow-up tasks.
- Non-review messages can send replies automatically when `AI_AUTO_REPLY_ENABLED=true`.
- Agent activity is stored in `ai_logs`.

Local behavior:

- If `OPENAI_API_KEY` is empty, the agent uses deterministic fallback classification and reply generation.
- If OpenAI is configured, reply generation uses `OPENAI_MODEL`.
- LangGraph is used when installed; the workflow has a sequential fallback for local host checks before Docker dependencies are installed.

Endpoints:

- `POST /api/v1/agents/messages/{message_id}/run`

Inbound WhatsApp webhooks and mock inbound messages trigger the message agent when:

```env
AI_AUTO_REPLY_ENABLED=true
```

