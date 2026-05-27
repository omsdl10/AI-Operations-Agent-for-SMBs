# Stage 7 Twilio WhatsApp Integration

Stage 7 adds WhatsApp messaging through Twilio.

Backend:

- `POST /api/v1/twilio/webhook`
- `POST /api/v1/twilio/status`
- `POST /api/v1/twilio/mock-inbound`
- `GET /api/v1/messages/conversations`
- `GET /api/v1/messages/conversations/{customer_id}`
- `POST /api/v1/messages/send`

Implemented:

- Inbound WhatsApp webhook handler.
- Customer lookup by phone number.
- Automatic customer creation for unknown inbound WhatsApp numbers.
- Message persistence with direction, channel, status, body, external ID, and timestamps.
- Outbound WhatsApp message service.
- Twilio status callback handler.
- Mock mode for local development.
- API-backed frontend conversation list and chat view.

## Local Mock Mode

Mock mode is enabled by default:

```env
TWILIO_MOCK_MODE=true
```

Create a mock inbound WhatsApp message:

```bash
curl -X POST http://localhost:8000/api/v1/twilio/mock-inbound \
  -F "from_number=+15550001111" \
  -F "body=Hi, can I book an appointment?"
```

Outbound messages from the frontend are stored locally and assigned a mock external ID.

## Twilio Configuration

Set these values in `.env` for real Twilio sending:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_MOCK_MODE=false
TWILIO_DEFAULT_BUSINESS_ID=your_business_id
```

In the Twilio Console WhatsApp Sandbox or sender settings, configure:

- Incoming message webhook: `https://your-domain.com/api/v1/twilio/webhook`
- Status callback URL: `https://your-domain.com/api/v1/twilio/status`
- Method: `POST`

For local webhook testing, expose the backend with a tunneling tool and use the public HTTPS URL.

