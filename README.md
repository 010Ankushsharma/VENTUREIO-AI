# VentureIQ AI — AI-Powered Due Diligence Platform

An enterprise-grade AI-powered Due Diligence Platform that enables Venture Capital firms,
Private Equity funds, Angel Investors, Investment Banks, Family Offices, Accelerators,
and Corporate Venture Arms to perform comprehensive startup evaluations in hours instead of weeks.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│        React · TypeScript · TailwindCSS · Recharts      │
└──────────────────────┬──────────────────────────────────┘
                       │  REST / WebSocket
┌──────────────────────▼──────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌────────────┐ ┌────────────┐ ┌──────────────────────┐ │
│  │  API Layer │ │  Services  │ │   AI Agent System    │ │
│  └────────────┘ └────────────┘ │  (LangGraph/Chain)   │ │
│                                │  8 Specialized Agents│ │
│                                └──────────────────────┘ │
│  ┌────────────┐ ┌────────────┐ ┌──────────────────────┐ │
│  │  Doc Proc  │ │    RAG     │ │   Forecasting        │ │
│  │  OCR/PDF   │ │  Qdrant    │ │  XGBoost/Prophet     │ │
│  └────────────┘ └────────────┘ └──────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Data Layer                                  │
│  PostgreSQL · Qdrant (Vector DB) · Redis · S3            │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone
git clone https://github.com/your-org/ventureiq-ai.git
cd ventureiq-ai

# Start all services
docker-compose up --build

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Project Structure

```
ventureiq-ai/
├── frontend/          # Next.js React TypeScript app
├── backend/           # FastAPI Python backend
│   ├── app/
│   │   ├── agents/    # 8 AI due-diligence agents
│   │   ├── api/       # REST endpoints
│   │   ├── core/      # Config, security, auth
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── services/  # Business logic
│   │   ├── rag/       # RAG pipeline (Qdrant)
│   │   ├── document_processing/  # PDF/OCR/Vision
│   │   └── forecasting/         # ML forecasting
├── infrastructure/    # Docker, K8s, Terraform
└── docs/              # Documentation
```

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Frontend    | Next.js, React, TypeScript, Tailwind |
| Backend     | FastAPI, Python 3.11+                |
| AI          | GPT-4/Claude, LangGraph, LangChain  |
| Vector DB   | Qdrant                               |
| Database    | PostgreSQL                           |
| Cache       | Redis                                |
| Storage     | AWS S3 / Azure Blob                  |
| Infra       | Docker, Kubernetes, Terraform        |
| Monitoring  | Prometheus, Grafana                  |

## License

Proprietary — All rights reserved.
