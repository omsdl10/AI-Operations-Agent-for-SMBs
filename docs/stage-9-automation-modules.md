# Stage 9 Automation Modules

Stage 9 adds the MVP automation worker system using APScheduler.

Implemented:

- Background automation cycle using APScheduler.
- Scheduled follow-up detection.
- Payment reminder scheduling.
- Appointment reminder scheduling.
- Overdue invoice detection.
- Notification scheduling and status updates.
- AI-assisted reminder copy with deterministic fallback text.
- Job logging through `ai_logs`.
- Manual automation trigger endpoint.
- Notification listing endpoint.

Scheduler configuration:

```env
AUTOMATION_SCHEDULER_ENABLED=true
AUTOMATION_INTERVAL_MINUTES=15
```

Endpoints:

- `POST /api/v1/automations/run-due`
- `GET /api/v1/automations/notifications`

Manual run:

```bash
curl -X POST http://localhost:8000/api/v1/automations/run-due \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Notes:

- APScheduler is used for the MVP. The service layer is isolated so the worker can move to Celery + Redis later.
- Notifications are stored in the `notifications` table.
- Automation job results are logged in `ai_logs`.
- OpenAI is optional. If `OPENAI_API_KEY` is empty, reminder copy uses safe fallback templates.

