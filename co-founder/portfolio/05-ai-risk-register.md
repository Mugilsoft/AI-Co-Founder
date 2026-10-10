# AI Risk Register

**Mugil Soft Solutions — Portfolio Asset | Week 5**

> A comprehensive AI risk register template with worked examples across multiple AI use cases. This register provides a structured approach to identifying, assessing, and managing risks associated with AI systems.

---

## How to Use This Register

1. **Identify** all risks associated with the AI system
2. **Describe** each risk clearly, including the mechanism of harm
3. **Identify** who is affected (users, affected people, organisation, society)
4. **Assess** severity (Critical / High / Medium / Low) and likelihood (Very Likely / Likely / Possible / Unlikely / Rare)
5. **Define** specific controls to mitigate each risk
6. **Assign** an owner responsible for implementing and monitoring controls
7. **Document** evidence that controls are implemented and effective
8. **Review** the register periodically and after any significant system changes

### Severity Scale

| Level | Description |
|-------|-------------|
| **Critical** | Severe harm to individuals, significant legal liability, or existential business risk |
| **High** | Substantial harm to individuals or significant financial/reputational damage |
| **Medium** | Moderate impact on individuals or noticeable financial/reputational consequences |
| **Low** | Minor inconvenience or easily remediated impact |

### Likelihood Scale

| Level | Description |
|-------|-------------|
| **Very Likely** | Expected to occur in normal operation |
| **Likely** | Will probably occur at some point |
| **Possible** | Could occur under certain conditions |
| **Unlikely** | Not expected but possible in unusual circumstances |
| **Rare** | Only in exceptional circumstances |

---

## Use Case 1: AI Hiring / CV Screening Tool

**System Description:** An AI system that screens job applicant CVs and assists recruiters by ranking candidates based on qualification match, experience, and skills.

| # | Risk | Description | Affected Users | Severity | Likelihood | Control | Owner | Evidence |
|---|------|-------------|----------------|----------|------------|---------|-------|----------|
| H-01 | **Gender Bias** | The model may learn to favour or penalise candidates based on gender-correlated features (e.g., names, pronouns, women's colleges, parental leave) present in historical hiring data | Job applicants (particularly women or non-binary individuals) | Critical | Likely | Remove gender-identifiable features from model input; test model outputs for gender-disaggregated pass rates; conduct periodic bias audits | AI Lead | Bias test results, feature list review, audit reports |
| H-02 | **Age Discrimination** | The model may use graduation years, technology stack vintage, or similar proxies to discriminate against older or younger candidates | Job applicants of certain age groups | High | Possible | Remove or normalise age-proxy features; test for age-correlated disparate impact; human review of borderline decisions | AI Lead | Feature engineering documentation, disparate impact analysis |
| H-03 | **Ethnic/Racial Bias** | Training data reflecting historical hiring patterns may perpetuate underrepresentation of certain ethnic groups | Job applicants from underrepresented ethnic groups | Critical | Possible | Audit training data demographics; test for disparate impact across ethnicity where permissible; ensure diverse evaluation panels | AI Lead + HR Lead | Data audit report, disparate impact analysis |
| H-04 | **Privacy Violation** | CV data contains extensive personal information (name, address, education, employment history) that must be protected under applicable data protection laws | All applicants | High | Possible | Implement access controls; encrypt data at rest and in transit; apply data minimisation; define retention periods; comply with DPDP Act 2023 | Data Protection Owner | Security controls documentation, data retention policy, DPDP checklist |
| H-05 | **Hallucination / Incorrect Ranking** | The AI may misinterpret CV content, hallucinate qualifications, or produce incorrect rankings | Applicants (wrongly rejected), recruiters (misled by inaccurate information) | High | Possible | Human review of all AI-assisted shortlists; confidence scoring; recruiter training on AI limitations | Recruitment Lead | Human review logs, error rate tracking |
| H-06 | **Lack of Explainability** | Candidates and recruiters cannot understand why a particular candidate was ranked high or low | Applicants, recruiters, hiring managers | Medium | Likely | Provide feature-importance explanations for rankings; document ranking criteria; enable recruiter overrides | AI Lead | Explainability output samples, recruiter feedback |
| H-07 | **No Appeal Mechanism** | Rejected candidates have no way to challenge an AI-influenced decision | Rejected applicants | High | Very Likely (if not designed) | Implement appeal process; inform candidates that AI is used; provide human review on request | HR Lead | Appeal process documentation, candidate communications |
| H-08 | **Automation Bias** | Recruiters may over-rely on AI rankings without performing their own evaluation of candidates | Applicants, recruiters | Medium | Likely | Train recruiters on AI limitations; present AI output as advisory, not deterministic; track override rates | Recruitment Lead | Training records, override rate metrics |

---

## Use Case 2: AI Healthcare Chatbot

**System Description:** An AI chatbot that answers patient health queries, provides general health information, and assists with appointment scheduling.

| # | Risk | Description | Affected Users | Severity | Likelihood | Control | Owner | Evidence |
|---|------|-------------|----------------|----------|------------|---------|-------|----------|
| HC-01 | **Medical Misinformation** | The AI may provide inaccurate or outdated medical information, potentially leading patients to take harmful actions | Patients | Critical | Possible | Restrict responses to verified medical knowledge base (RAG); include mandatory disclaimers; prohibit diagnostic or treatment recommendations | Clinical Lead | Knowledge base review, response audit, disclaimer verification |
| HC-02 | **Failure to Escalate** | The AI may fail to recognise emergency or crisis situations (e.g., symptoms of heart attack, stroke, self-harm) requiring immediate human intervention | Patients in medical emergencies | Critical | Possible | Implement crisis keyword detection; mandatory escalation to human for emergency indicators; fallback to emergency service contact information | Clinical Lead + AI Lead | Crisis detection test results, escalation logs |
| HC-03 | **Patient Data Privacy** | Health data is highly sensitive. Unauthorised access, leakage, or misuse of patient health information could cause significant harm | Patients | Critical | Possible | End-to-end encryption; strict access controls; data minimisation; no storage of health data beyond session; comply with applicable health data regulations | Data Protection Owner | Security audit, encryption verification, data flow diagram |
| HC-04 | **Hallucination** | The AI may generate plausible-sounding but fabricated medical information (e.g., inventing drug names, dosages, or interactions) | Patients | Critical | Likely | Use RAG with verified medical sources only; implement factual grounding checks; include confidence indicators; require medical professional review for clinical content | AI Lead | RAG evaluation results, hallucination testing, medical review logs |
| HC-05 | **Bias in Health Recommendations** | The AI may provide recommendations biased towards certain demographic groups if training data is unrepresentative | Patients from underrepresented demographics | High | Possible | Audit training data for demographic representation; test response quality across demographic scenarios; include diverse medical knowledge sources | AI Lead + Clinical Lead | Data diversity audit, demographic testing results |
| HC-06 | **Over-Reliance by Patients** | Patients may treat AI responses as definitive medical advice and delay seeking professional care | Patients | High | Likely | Prominent disclaimers that AI is not a substitute for professional medical advice; recommend professional consultation for clinical concerns; limit scope to general information and scheduling | Product Lead | Disclaimer presence verification, scope limitation documentation |

---

## Use Case 3: AI Customer Support System

**System Description:** An AI-powered customer support system that handles customer queries, provides product information, processes simple requests, and escalates complex issues to human agents.

| # | Risk | Description | Affected Users | Severity | Likelihood | Control | Owner | Evidence |
|---|------|-------------|----------------|----------|------------|---------|-------|----------|
| CS-01 | **Incorrect Information** | The AI may provide wrong product details, pricing, return policies, or account information | Customers | Medium | Likely | Ground responses in up-to-date knowledge base (RAG); implement response validation; track accuracy metrics; regular knowledge base updates | Product Lead | Accuracy metrics, knowledge base update log |
| CS-02 | **Failure to Escalate** | Complex, emotional, or high-stakes issues may not be properly escalated to human agents | Customers with complex issues | Medium | Possible | Define escalation triggers (sentiment, topic complexity, repeated failures); implement mandatory escalation paths; monitor escalation rates | Support Lead | Escalation trigger configuration, escalation rate metrics |
| CS-03 | **Customer Data Exposure** | The AI may inadvertently reveal other customers' data or internal system information in responses | Customers, organisation | High | Unlikely | Strict data access controls; response filtering; penetration testing for data leakage; session isolation | Security Lead | Penetration test results, access control audit |
| CS-04 | **Prompt Injection** | Malicious users may attempt to manipulate the AI through adversarial inputs to extract confidential information or alter system behaviour | Organisation, other customers | High | Possible | Input sanitisation; prompt injection testing; system prompt protection; regular red teaming | Security Lead + AI Lead | Red team test results, injection test coverage |
| CS-05 | **Language/Accessibility Bias** | The AI may perform poorly for users communicating in non-dominant languages, dialects, or with accessibility needs | Customers with diverse language or accessibility requirements | Medium | Possible | Test performance across supported languages; provide alternative human support channels; implement accessibility features | Product Lead | Multi-language test results, accessibility compliance |
| CS-06 | **Reputational Risk** | The AI may generate inappropriate, offensive, or brand-damaging responses | Organisation, customers | High | Unlikely | Content safety filters; brand guidelines in system prompt; response quality monitoring; human review of flagged conversations | Support Lead + Marketing Lead | Content filter configuration, flagged conversation review logs |

---

## Use Case 4: AI Clinical Decision Support & Patient Record Analytics for Medical Clinics

**System Description:** An AI Clinical Decision Support System (CDSS) for medical clinics that analyzes electronic health records (EHR), lab reports, and clinical notes to assist attending physicians with diagnostic possibilities, risk stratification, and differential diagnosis recommendations.

| # | Risk | Description | Affected Users | Severity | Likelihood | Control | Owner | Evidence |
|---|------|-------------|----------------|----------|------------|---------|-------|----------|
| CD-01 | **Diagnostic Misclassification / False Negatives** | AI misses a critical clinical indicator or suggests an incorrect differential diagnosis, risking patient harm or delayed critical intervention | Patients, attending physicians | Critical | Possible | Enforce mandatory Human-in-the-Loop (HITL) physician sign-off; AI outputs strictly advisory; confidence intervals displayed; doctor override mandatory | Clinical Director + AI Lead | Clinical validation test logs, physician override logs, error rate audits |
| CD-02 | **Health Data Leakage & DPDP Violation** | Exposure or unauthorized processing of sensitive personal data (EHR, diagnostic reports, PII) in violation of India's DPDP Act 2023 | Clinic patients | Critical | Possible | Field-level de-identification/anonymization before model inference; AES-256 encryption at rest and in transit; role-based access; zero data retention for training without consent | Data Protection Officer | DPDP compliance certificate, encryption verification, penetration test reports |
| CD-03 | **Demographic & Pathological Bias** | Model performs with varying accuracy across patient age brackets, genders, socioeconomic backgrounds, or rare clinical presentations | Patients from underrepresented cohorts | High | Possible | Pre-deployment bias audit across demographic cohorts; stratified test datasets; clear model cards declaring performance boundaries | Governance Lead + AI Lead | Pre-deployment bias audit report, demographic performance matrix |
| CD-04 | **Physician Automation Bias** | Over-reliance by clinicians leading to rubber-stamping AI diagnostic outputs without independent critical clinical evaluation | Clinic patients, medical staff | High | Likely | Interface requires explicit physician confirmation of reviewed indicators; un-preselected checkboxes; continuous monitoring of physician review time | Product Lead + Clinical Director | Clinician interaction logs, dwell-time analytics, user training records |
| CD-05 | **Hallucination of Medical Protocols & Dosages** | Generative components invent non-existent contraindications, incorrect pharmacological dosages, or outdated clinical guidelines | Patients receiving prescribed treatments | Critical | Possible | RAG grounding strictly constrained to accredited clinical compendia (e.g., ICMR, WHO, Pharmacopoeia); deterministic guardrails on dosage ranges | AI Lead + Medical Safety Officer | Factual grounding benchmarks, dosage limit guardrail test results |
| CD-06 | **Data Drift from Clinical Equipment & Lab Variations** | Calibration differences in clinic lab equipment or imaging protocols degrade AI diagnostic precision over time | Clinic patients, diagnostic labs | High | Likely | Ongoing drift detection pipeline; periodic retraining with calibrated multi-clinic datasets; quarterly model accuracy re-certification | MLOps Lead | Model drift dashboard, quarterly re-certification reports |

---

## Risk Register Maintenance

| Activity | Frequency | Owner |
|----------|-----------|-------|
| Review existing risks and controls | Quarterly | AI Lead |
| Add new risks from incident reports | As incidents occur | AI Lead |
| Update severity/likelihood based on monitoring data | Quarterly | AI Lead |
| Verify control effectiveness | Semi-annually | Governance Lead |
| Full risk register audit | Annually | Governance Lead |
| Post-deployment risk reassessment | After each major release | Project Lead |

---

## Blank Template

Copy this template for new AI systems:

| # | Risk | Description | Affected Users | Severity | Likelihood | Control | Owner | Evidence |
|---|------|-------------|----------------|----------|------------|---------|-------|----------|
| | | | | | | | | |

---

*Version 1.0 — Mugil Soft Solutions*
*This risk register is for professional and educational purposes. Risk assessments should be validated by domain experts and updated as AI systems evolve.*
