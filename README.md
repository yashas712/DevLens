# DevLens

> **Developer Intelligence & GitHub Portfolio Analytics Platform**

A database-centric web application that transforms raw GitHub activity into meaningful insights, developer scores, and professional portfolio reports.

---

## Overview

DevLens goes beyond traditional GitHub profile viewers by focusing on **analytics rather than browsing**. It collects GitHub data, stores it in a normalized PostgreSQL database, and uses advanced SQL queries, aggregations, and trend analysis to generate rich insights.

The platform answers questions that GitHub itself cannot easily answer:

- Which repositories are growing the fastest?
- How consistent is a developer’s activity?
- Which programming language is becoming dominant over time?
- What type of developer profile does someone have?
- How has coding activity evolved over months/years?

---

## Key Features

### Core Features
- **GitHub OAuth Login** – Secure authentication using GitHub accounts
- **Repository Analytics** – Stars, forks, language breakdown, growth trends
- **Commit Analytics** – Commit frequency, streaks, contribution patterns
- **Developer Intelligence** – Activity score, productivity metrics, growth tracking
- **Interactive Dashboard** – Visual charts, heatmaps, and timelines
- **Developer Comparison** – Side-by-side comparison of two developers
- **Portfolio Reports** – Generate professional summaries and insights

### Data Insights
- Language dominance and evolution over time
- Repository health and popularity trends
- Coding consistency and productivity streaks
- Collaboration and contribution patterns

---

## Proposed Architecture

```
GitHub API
    │
    ▼
Data Collection Service
    │
    ▼
PostgreSQL Database (normalized schema)
    │
    ▼
Analytics Engine (SQL + Views + Stored Procedures)
    │
    ▼
FastAPI Backend (REST API)
    │
    ▼
React + Tailwind Dashboard
```

---

## Technology Stack

| Layer       | Technologies                          |
|-------------|---------------------------------------|
| **Frontend**    | React, Vite, Tailwind CSS, Recharts, React Router |
| **Backend**     | FastAPI, SQLAlchemy, Pydantic, Alembic |
| **Database**    | PostgreSQL (Neon)                     |
| **Auth**        | GitHub OAuth                          |
| **Deployment**  | Vercel (Frontend), Render (Backend), Neon (Database) |
| **Tools**       | GitHub Actions, dbdiagram.io, Figma   |

---

## Database Highlights

- Fully normalized relational schema (up to BCNF)
- Advanced SQL features: Window functions, CTEs, Views, Stored Procedures, Triggers
- Indexing strategy for performance
- Efficient data ingestion from GitHub API

---

## Project Roadmap

| Sprint | Focus Area                          | Duration     |
|--------|-------------------------------------|--------------|
| 1      | Requirements, ERD, Schema           | 2 weeks      |
| 2      | GitHub Integration & Authentication | 3 weeks      |
| 3      | Data Ingestion & Core Analytics     | 3 weeks      |
| 4      | Dashboard UI & Visualization        | 3 weeks      |
| 5      | Testing, Optimization & Deployment  | 2 weeks      |
| 6      | Documentation & Final Release       | 3 weeks      |

---

## Getting Started (Coming Soon)

Once the project is set up, you will be able to:

```bash
# Clone the repository
git clone https://github.com/your-org/DevLens.git
cd DevLens

# Follow setup instructions in the docs folder
```

---

## Stretch Goals (Future)

- AI-generated developer summaries
- PDF portfolio & resume generation
- Organization-level analytics
- Recommendation engine for repositories

---

## What Makes DevLens Different?

- Strong emphasis on **database engineering** and advanced SQL
- Real-world API integration with proper rate limiting and caching
- Clean separation between data collection, storage, analytics, and presentation
- Professional development practices (Git flow, documentation, CI/CD)
- Built entirely on free-tier services

---

## License

This project is licensed under the MIT License.

---

**Built with ❤️ as a Database Systems course project.**