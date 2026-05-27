# Stage 10 Daily Business Summary Agent

Stage 10 adds the daily business summary workflow.

Workflow nodes:

1. `collect_daily_data_node`
2. `summarize_sales_node`
3. `summarize_customers_node`
4. `summarize_payments_node`
5. `summarize_appointments_node`
6. `recommendation_engine_node`
7. `generate_final_summary_node`

Implemented:

- LangGraph daily summary workflow with local sequential fallback.
- Daily metric collection for leads, conversations, payments, overdue invoices, follow-ups, and appointments.
- AI recommendations with deterministic fallback.
- Summary storage in `daily_summaries`.
- AI activity logging in `ai_logs`.
- Manual summary generation endpoint.
- Summary history endpoint.
- Daily scheduler hook at 23:55 UTC.
- Frontend summary dashboard.
- Downloadable text reports.

Endpoints:

- `POST /api/v1/summaries/generate`
- `GET /api/v1/summaries`
- `GET /api/v1/summaries/{summary_date}`

Manual generation:

```bash
curl -X POST http://localhost:8000/api/v1/summaries/generate \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"summary_date": null}'
```

