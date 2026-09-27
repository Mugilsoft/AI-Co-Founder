# DPDP + AI Checklist

**Mugil Soft Solutions — Portfolio Asset | Week 4**

> A practical checklist for evaluating AI projects against India's Digital Personal Data Protection Act, 2023 (DPDP Act). This checklist helps teams identify data protection requirements and risks when building or deploying AI systems that process personal data of Indian data principals.

---

## Important Disclaimer

> **This document is for professional and educational purposes only. It does not constitute legal advice.** The DPDP Act 2023 is subject to ongoing rule-making, interpretation, and enforcement developments. Where legal compliance is critical, engage qualified legal professionals with expertise in Indian data protection law.

---

## Overview of the DPDP Act, 2023

India's **Digital Personal Data Protection Act, 2023** establishes a framework for the processing of digital personal data. Key concepts include:

| Concept | Meaning |
|---------|---------|
| **Data Principal** | The individual whose personal data is being processed |
| **Data Fiduciary** | The entity that determines the purpose and means of processing personal data |
| **Significant Data Fiduciary** | A data fiduciary designated by the government based on volume, sensitivity, or risk of data processing |
| **Data Processor** | An entity that processes personal data on behalf of a data fiduciary |
| **Consent** | Free, specific, informed, unconditional, and unambiguous indication of the data principal's wishes |
| **Legitimate Uses** | Specified purposes for which personal data may be processed without explicit consent (e.g., state functions, employment, emergencies) |
| **Data Protection Board of India** | The authority established to oversee compliance and adjudicate complaints |

---

## DPDP + AI Checklist

### Section 1: Data Mapping

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 1.1 | What personal data does the AI system collect or receive? | You cannot protect data you have not identified. The DPDP Act requires understanding what personal data is being processed. | Data inventory listing all personal data fields, sources, and formats | ☐ |
| 1.2 | Who are the data principals (individuals) whose data is processed? | The Act grants rights to data principals. You must know who they are to fulfil those rights. | Documentation identifying categories of data principals (e.g., customers, employees, job applicants) | ☐ |
| 1.3 | Where does the personal data originate? | Understanding data sources helps assess data quality, consent chains, and lawful processing basis. | Data flow diagram showing data sources, collection points, and transfers | ☐ |
| 1.4 | Does the AI system process children's data (under 18)? | The DPDP Act imposes additional restrictions on processing children's data, including verifiable parental consent and a prohibition on tracking, behavioural monitoring, and targeted advertising directed at children. | Age verification mechanism documentation, parental consent process | ☐ |
| 1.5 | Is personal data transferred outside India? | The Act permits cross-border transfers to countries not restricted by the Central Government. Restricted destinations require compliance verification. | Record of cross-border data transfers, destination countries, and compliance basis | ☐ |

---

### Section 2: Purpose Limitation

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 2.1 | What is the stated purpose for processing personal data? | The DPDP Act requires that personal data be processed only for a lawful purpose — the purpose for which consent was obtained or a legitimate use applies. | Documented purpose statement for each data processing activity | ☐ |
| 2.2 | Is the AI system using personal data only for the stated purpose? | Purpose limitation prevents mission creep — using data collected for one purpose in a different AI application. | Audit trail mapping data use to stated purposes | ☐ |
| 2.3 | If the AI system uses personal data for training, was this included in the stated purpose? | Using customer data to train AI models may constitute a different purpose than the one for which data was originally collected. | Training data governance documentation, consent records covering AI training use | ☐ |
| 2.4 | Does the AI system generate new personal data or inferences about individuals? | AI-generated inferences (e.g., credit risk scores, health predictions) may themselves constitute personal data requiring protection. | Documentation of AI-generated data types and their treatment under data protection policies | ☐ |

---

### Section 3: Lawful Processing

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 3.1 | What is the lawful basis for processing personal data? | The DPDP Act requires either consent or a specified legitimate use as the basis for processing. Processing without a lawful basis is a violation. | Documented lawful basis for each processing activity | ☐ |
| 3.2 | If relying on consent — is the consent free, specific, informed, unconditional, and unambiguous? | The Act sets a high standard for valid consent. Bundled, coerced, or vague consent may not be valid. | Consent collection mechanism, consent text, records of consent | ☐ |
| 3.3 | If relying on consent — can the data principal easily withdraw consent? | The Act provides the right to withdraw consent at any time. The process for withdrawal must be as easy as giving consent. | Consent withdrawal mechanism and documentation | ☐ |
| 3.4 | If relying on a legitimate use — which specific legitimate use applies? | Legitimate uses are narrowly defined in the Act (e.g., state functions, employment, medical emergencies). Claiming a legitimate use that does not apply is a violation. | Legal analysis identifying the applicable legitimate use provision | ☐ |
| 3.5 | If consent is withdrawn, can the AI system continue to function without that individual's data? | Systems must be designed to handle consent withdrawal gracefully — including removing data from models if feasible, or documenting why removal is technically infeasible. | Technical documentation of consent withdrawal handling | ☐ |

---

### Section 4: Data Minimisation

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 4.1 | Is the AI system collecting only the personal data necessary for the stated purpose? | Data minimisation reduces risk. Collecting unnecessary data increases breach impact, storage costs, and regulatory exposure. | Data inventory review showing necessity justification for each data field | ☐ |
| 4.2 | Can the AI system achieve its purpose with anonymised or aggregated data instead of personal data? | If the purpose can be achieved without personal data, processing personal data may not be justified. | Technical assessment of anonymisation feasibility | ☐ |
| 4.3 | Is personal data retained only for as long as necessary? | The DPDP Act requires erasure of personal data when it is no longer needed for the stated purpose (unless legally required to retain it). | Data retention policy, automated deletion mechanisms | ☐ |
| 4.4 | Does the AI training dataset contain personal data that could be removed or anonymised without degrading model performance? | Using personal data in training when non-personal alternatives exist may violate data minimisation principles. | Training data audit, anonymisation assessment | ☐ |

---

### Section 5: Data Principal Rights

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 5.1 | Can data principals access information about how their personal data is being processed? | The Act grants data principals the right to obtain information about data processing, including a summary of personal data and processing activities. | Data access request mechanism and response process | ☐ |
| 5.2 | Can data principals request correction or erasure of their personal data? | The Act provides rights to correction of inaccurate/misleading data, completion of incomplete data, updating of outdated data, and erasure. | Correction and erasure request mechanism and fulfillment process | ☐ |
| 5.3 | Can data principals nominate another person to exercise their rights? | The Act provides for nomination of another individual to exercise data principal rights in certain circumstances (e.g., death, incapacity). | Nomination mechanism documentation | ☐ |
| 5.4 | How does the AI system handle a data principal's right to grievance redressal? | Data fiduciaries must provide a mechanism for data principals to register grievances, with responses within the prescribed time period. | Grievance redressal process, contact information, response timelines | ☐ |
| 5.5 | If the AI system has made a decision based on a data principal's personal data, can the data principal access the reasoning? | While the DPDP Act does not explicitly mandate algorithmic transparency, the right to information about processing combined with general accountability principles supports providing meaningful explanations. | Explainability mechanism for AI decisions | ☐ |

---

### Section 6: Accountability

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 6.1 | Who is the designated data fiduciary responsible for this AI system's data processing? | The DPDP Act places obligations on the data fiduciary. Clear designation ensures someone is accountable. | Named data fiduciary and organisational accountability structure | ☐ |
| 6.2 | Has a Data Protection Officer been appointed (if required as a Significant Data Fiduciary)? | Significant Data Fiduciaries must appoint a DPO based in India. | DPO appointment documentation (if applicable) | ☐ |
| 6.3 | Are there adequate security safeguards to prevent personal data breaches? | The Act requires data fiduciaries to implement reasonable security safeguards. A breach may require notification to the Data Protection Board and affected data principals. | Security controls documentation, encryption standards, access controls | ☐ |
| 6.4 | Is there a personal data breach notification process? | The Act requires notification of breaches to the Data Protection Board of India in the prescribed form and manner. | Breach notification procedure, response team, notification templates | ☐ |
| 6.5 | Are data processing agreements in place with third-party data processors? | Data fiduciaries remain responsible for data processed by processors on their behalf. Contracts must ensure processors meet data protection requirements. | Data processing agreements with all relevant third parties | ☐ |

---

### Section 7: Human Oversight and AI-Specific Considerations

| # | Question | Why It Matters | Evidence Required | Status |
|---|----------|---------------|-------------------|--------|
| 7.1 | Can a human review and override AI decisions that significantly affect data principals? | While not explicitly mandated by the DPDP Act, human oversight is a responsible AI best practice that supports accountability and fairness. | Human review mechanism documentation for significant AI decisions | ☐ |
| 7.2 | Is the AI system's use of personal data documented in sufficient detail for regulatory review? | The Data Protection Board may request information about data processing activities. Inadequate documentation hinders compliance. | Comprehensive data processing documentation | ☐ |
| 7.3 | Has the AI system been assessed for potential disproportionate impact on any group? | While not explicitly a DPDP Act requirement, fairness considerations support compliance with the Act's general principles and reduce risk of complaints. | Fairness assessment documentation | ☐ |
| 7.4 | If the AI system is a Significant Data Fiduciary system, has a Data Protection Impact Assessment been conducted? | Significant Data Fiduciaries are required to conduct periodic data protection impact assessments. | DPIA documentation (if applicable) | ☐ |
| 7.5 | Is there a process for periodic review of the AI system's data protection compliance? | Ongoing compliance requires regular review, particularly as the AI system evolves, data volumes change, and rules under the Act are issued. | Periodic review schedule and audit records | ☐ |

---

## Summary Checklist Status Tracker

| Section | Items | Completed | Status |
|---------|-------|-----------|--------|
| 1. Data Mapping | 5 | ☐ | Not Started |
| 2. Purpose Limitation | 4 | ☐ | Not Started |
| 3. Lawful Processing | 5 | ☐ | Not Started |
| 4. Data Minimisation | 4 | ☐ | Not Started |
| 5. Data Principal Rights | 5 | ☐ | Not Started |
| 6. Accountability | 5 | ☐ | Not Started |
| 7. Human Oversight & AI | 5 | ☐ | Not Started |
| **Total** | **33** | | |

---

## Key References

- Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)
- Ministry of Electronics and Information Technology (MeitY) — for rules and notifications under the Act

---

*Version 1.0 — Mugil Soft Solutions*
*This checklist is for professional and educational purposes only. It does not constitute legal advice. The DPDP Act 2023 is subject to ongoing rule-making and interpretation. Engage qualified legal professionals for compliance assurance.*
