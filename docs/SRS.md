# Software Requirements Specifications (SRS)

DevLens - Developer Intelligence & GitHub Portfolio Analytics Platform
Version 0.1: (Phase 1 Draft)
Emphasis: Database Systems

## Purpose

DevLens collects, stores and analyzes GitHub activity data to produce insights that GitHub's own UI doesn't show - developer consistency, growth trends, language dominance and a computed "developer score". This document defines what the system must do (functional requirements) and the conditions it must operate under (non-functional requirements), so scope is well defines for the duration of the development.

## Functional Requirements

### Authentication

1. Users must be able to login via GitHub OAuth
2. The system must store a session token and refresh it as needed.
3. Users must be able to log out and revoke access

### Repository Collection

1. On first login, the system must fetch the user's repositories (name, stars, forks, primary language, creation date)
2. The system must store brach and language breakdown data per repository.
3. Repository data must be refreshable on demand (manual sync) and, as a future goal, on a schedule.

### Commit Analysis

1. The system must ingest commit history per repository (author, timestamp, additions, deletion, messages).
2. The system must compute commit frequency over time (daily/weekly).
3. The system must compute the user's current and longest commit streak.

### Developer Analysis

1. The system must compute a developer score from a weighted combination of activity, consistency and repository growth.
2. The system must classify dominant languages per user over time.
3. The system must expose a scoring breakdown, not just a final number.

### Dashboard

1. The system must display a summary view (score, top languages, recent activity).
2. The system must render a commit heatmap (calendar styled).
3. The system must render growth/trend charts per repository.

### Comparison

Users must be able to compare two developers side-by-side on the same metrics.

### Reports

The system must generate a shareable summary report of a developer's profile (web view or PDF in the future goals).

## Non Functional Requirements

### Rate Limits

GitHub's REST API allows 5,000 authenticated requests/hour per user. Sync jobs must respect this and back off gracefully rather than failing.

### Performance

Dashboard queries must return in under 2 seconds for a developer with up to ~5,000 commits across ~50 repositories.

### Cost

All infrastructure must run on free tiers (Vercel, Render, Neon Postgres).

### Data Freshness

Data does not need to be real time. A manual or periodic sync is acceptable, for now.

### Security 

OAuth tokens must never be exposed to the frontend or logged in plain text.


## Out of Scope

These are future goals that may be implemented after the core scope has been reached.

1. AI generated portfolio summary
2. Resume/PDF generation
3. Scheduled background sync (manual sync is the baseline).

## Assumptions/Constraints

Users must have a public (or accessible) GitHub account. Private repo will not be considered while doing analysis.

## Success Criteria

A user is able to login, sync their GitHub data, and see a populated dashboard.

The database demonstrates normalisation, at least one view, one stored procedure, one trigger and appropriate indexing.

The comparison feature works for any two arbitrary logged in users.

All documentation deliverables listed in the project proposal exist.



# Note

Database Schema live on Neon.
ER Diagram is present under docs/ER_Diagram.png.
