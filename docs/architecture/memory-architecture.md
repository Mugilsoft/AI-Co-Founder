# Memory Architecture — Mugil AI Co-Founder System

## 1. Executive Summary

The **Mugil AI Co-Founder Memory Architecture** ensures long-term continuity, contextual awareness, and persistent knowledge retention across all co-founder interactions. The memory system is structured into five distinct domain stores, maintained under strict privacy and security constraints.

---

## 2. Five Domain Memory Stores

```
                      ┌─────────────────────────────────┐
                      │    Co-Founder Memory Engine     │
                      └────────────────┬────────────────┘
                                       │
        ┌──────────────┬───────────────┼───────────────┬──────────────┐
        ▼              ▼               ▼               ▼              ▼
  ┌───────────┐  ┌───────────┐   ┌───────────┐   ┌───────────┐  ┌───────────┐
  │  Company  │  │Governance │   │ Technical │   │ Products  │  │ Customers │
  │  Memory   │  │  Memory   │   │  Memory   │   │  Memory   │  │  Memory   │
  └───────────┘  └───────────┘   └───────────┘   └───────────┘  └───────────┘
```

### 2.1 Company Memory (`memory/company.md`)
- **Scope**: Core corporate identity, mission, tagline, brand guidelines, target service offerings, strategic milestones, and organizational roadmap.
- **Key Information Retained**:
  - Company positioning (*Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.*).
  - Portfolio service catalog (Software, Web, Mobile, Desktop, AI/ML, RAG, ERP, Cloud, Healthcare Tech, AI Governance).
  - Long-term strategic targets and business milestones.

### 2.2 Governance Memory (`memory/governance.md`)
- **Scope**: Decisions made during AI Governance Gates, risk registers, compliance reviews, and ethical policy iterations.
- **Key Information Retained**:
  - Historical AI Risk Assessments and mitigated risks.
  - DPDP Act compliance audit logs and evidence mapping.
  - Bias audit outcomes and fairness thresholds established across client projects.

### 2.3 Technical Memory (`memory/technical.md`)
- **Scope**: System architecture records (ADRs), tech stack standards, performance baselines, security guidelines, and CI/CD conventions.
- **Key Information Retained**:
  - Preferred stack selections (React, Vite, Node.js, Python, PostgreSQL, BigQuery, TailwindCSS/Vanilla CSS).
  - Code refactoring standards and security hardening checklists.
  - Infrastructure templates and deployment pipelines.

### 2.4 Products Memory (`memory/products.md`)
- **Scope**: Active and pipeline product concepts, Product Requirement Documents (PRDs), feature roadmaps, MVP definitions, and backlog items.
- **Key Information Retained**:
  - Feature specifications and user story backlogs.
  - Prioritized product roadmap (Now, Next, Later).
  - Technical debt tracking for internal tools and SaaS products.

### 2.5 Customers Memory (`memory/customers.md`)
- **Scope**: Anonymized client project summaries, domain verticals served, feedback patterns, and proposal engagement metrics.
- **Key Information Retained**:
  - Service delivery outcomes across software and AI projects.
  - General industry requirements (e.g., Healthcare HIPAA/DPDP requirements, ERP integration patterns).
  - *Strict Rule*: No unmasked PII, credentials, or proprietary client code is stored.

---

## 3. Memory Access & Update Protocol

### 3.1 Read Operations
- Before processing complex strategic, architectural, or governance queries, the Co-Founder system reads the corresponding domain memory file to ensure context alignment.

### 3.2 Write & Mutation Protocol
- **Explicit Decision Logging**: Memory is updated when a key business, technical, or governance decision is finalized.
- **Append-Only Event Records**: Log entries include timestamp, decision summary, rationale, and responsible agent.
- **Periodic Pruning & Summarization**: Monthly consolidation of raw logs into high-level knowledge representations to avoid context overload.

---

## 4. Security, Privacy & Data Compliance

1. **No Secrets or Credentials**: Under no circumstances shall API keys, passwords, database credentials, or tokens be stored in memory files.
2. **PII Masking**: Customer names and personal contact details are redacted or hashed before entry into `customers.md`.
3. **DPDP Compliance**: All data stored aligns with India's DPDP Act 2023 data minimisation and purpose limitation principles.
