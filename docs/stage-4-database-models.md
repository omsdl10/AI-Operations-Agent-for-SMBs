# Stage 4 Database Models

Stage 4 adds the production database foundation:

- SQLAlchemy models for users, businesses, customers, leads, messages, follow-ups, invoices, appointments, daily summaries, AI logs, and notifications.
- Relationships, foreign keys, timestamps, and query indexes.
- Alembic configuration and an initial schema migration.
- Seed script with sample business data.

Run migrations:

```bash
cd backend
alembic upgrade head
```

Load sample data:

```bash
python scripts/seed.py
```

Sample login:

- Email: `owner@example.com`
- Password: `password123`

