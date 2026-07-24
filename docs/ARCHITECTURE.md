# VentureIQ AI — Architecture

## Multi-Agent System

```
Document Upload → Document Processing → Chunking → Embedding → Qdrant

                ┌─────────────────────────┐
                │ Startup Understanding   │  Agent 1
                └────────────┬────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                      │
  ┌────▼─────┐        ┌─────▼────┐         ┌──────▼──────┐
  │Financial │        │ Market   │         │Competitive  │  Agents 2-4
  └────┬─────┘        └─────┬────┘         └──────┬──────┘
       │                     │                      │
       └─────────────────────┼─────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │                              │
        ┌─────▼─────┐               ┌───────▼──────┐
        │   Risk    │               │    Fraud     │  Agents 5-6
        └─────┬─────┘               └───────┬──────┘
              │                              │
              └──────────────┬───────────────┘
                             │
                    ┌────────▼────────┐
                    │   Valuation     │  Agent 7
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Recommendation  │  Agent 8
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Report Gen     │
                    └─────────────────┘
```

## Scoring Framework

| Dimension        | Weight |
|-----------------|--------|
| Team             | 20%    |
| Product          | 15%    |
| Market           | 20%    |
| Traction         | 20%    |
| Financial Health | 15%    |
| Risk Profile     | 10%    |

Final Score: 0-100
