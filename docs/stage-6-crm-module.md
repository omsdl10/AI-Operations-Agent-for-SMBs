# Stage 6 CRM Module

Stage 6 adds the CRM feature set:

- Customer CRUD API with notes, tags, search, tag filtering, and pagination.
- Lead CRUD API with pipeline status, customer assignment, source, value, priority score, search, status filtering, and pagination.
- Protected CRM routes scoped to the authenticated user business.
- Repository and service layer implementation for customers and leads.
- Frontend customer and lead tables backed by the API.
- Customer and lead create forms.
- Customer and lead detail pages with edit forms.
- Safe delete behavior that preserves historical linked records by clearing CRM references.

Lead statuses:

- `new`
- `contacted`
- `interested`
- `converted`
- `lost`

CRM API endpoints:

- `GET /api/v1/customers`
- `POST /api/v1/customers`
- `GET /api/v1/customers/{customer_id}`
- `PUT /api/v1/customers/{customer_id}`
- `DELETE /api/v1/customers/{customer_id}`
- `GET /api/v1/leads`
- `POST /api/v1/leads`
- `GET /api/v1/leads/{lead_id}`
- `PUT /api/v1/leads/{lead_id}`
- `DELETE /api/v1/leads/{lead_id}`

