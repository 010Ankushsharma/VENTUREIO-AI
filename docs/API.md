# VentureIQ AI — API Documentation

Base URL: `http://localhost:8000/api/v1`

## Authentication

### POST /auth/register
Register a new user.

### POST /auth/login
Login and receive JWT token.

### GET /auth/me
Get current user profile.

## Deals

### POST /deals/
Create a new deal.

### GET /deals/
List all deals (paginated).

### GET /deals/{id}
Get deal details.

### PATCH /deals/{id}
Update a deal.

### DELETE /deals/{id}
Delete a deal.

## Documents

### POST /documents/upload/{deal_id}
Upload a document (multipart form).

### GET /documents/deal/{deal_id}
List documents for a deal.

## Analysis

### POST /analysis/trigger
Trigger AI analysis for a deal.

### GET /analysis/deal/{deal_id}
List all analyses for a deal.

## Reports

### POST /reports/generate/{deal_id}
Generate due diligence report.

### GET /reports/deal/{deal_id}
List reports for a deal.

## Dashboard

### GET /dashboard/stats
Get dashboard statistics.

### GET /dashboard/pipeline
Get deal pipeline.

---

Full interactive docs: http://localhost:8000/docs
