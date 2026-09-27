# AI Governance Review — AI Hiring Tool

**Mugil Soft Solutions — Portfolio Asset | Week 8 (Capstone)**

> A comprehensive AI governance review of an AI-assisted hiring tool. This case study evaluates the system against five global governance frameworks, identifies risks, proposes controls, and demonstrates the governance methodology that Mugil Soft Solutions applies to high-risk AI projects.

---

## Executive Summary

This governance review evaluates a proposed **AI-assisted CV screening and candidate ranking tool** intended to help recruiters process high volumes of job applications more efficiently. The tool uses machine learning to analyse CVs, extract qualifications and experience, and produce a relevance ranking against job specifications.

**Key Finding:** AI-assisted hiring is a **high-risk AI application** that directly affects individuals' employment opportunities. It requires rigorous governance controls across fairness, transparency, privacy, accountability, and human oversight. Multiple global frameworks — including the EU AI Act — classify this type of system as high-risk, requiring enhanced governance measures.

**Recommendation:** The system should not be deployed until the controls identified in this review are implemented and verified. Deployment should be preceded by explicit founder approval following a complete AI Governance Gate review.

---

## 1. Problem Statement

### Business Context
A company receives thousands of CVs for each open position. Manual screening is time-consuming and inconsistent. The company proposes using AI to:

- Parse and extract information from CVs
- Compare candidate qualifications against job requirements
- Produce a ranked shortlist for recruiter review
- Reduce time-to-hire and improve screening consistency

### AI System Description

| Aspect | Detail |
|--------|--------|
| **System Type** | Machine learning classification and ranking model |
| **Input** | Job specification + candidate CVs (PDF/DOCX) |
| **Output** | Ranked list of candidates with relevance scores and key qualification matches |
| **Intended Use** | Assist recruiters in shortlisting — not replace human decision-making |
| **Decision Authority** | Advisory only — final hiring decisions remain with human recruiters and hiring managers |

---

## 2. Users and Affected People

| Stakeholder | Role | Interest | Risk Exposure |
|-------------|------|----------|---------------|
| **Job Applicants** | Data principals; affected people | Fair evaluation, privacy, transparency, right to appeal | **High** — AI directly influences their employment opportunity |
| **Recruiters** | Primary users | Efficient, accurate shortlisting; confidence in AI recommendations | **Medium** — Reliance on potentially biased or incorrect AI outputs |
| **Hiring Managers** | Decision-makers | Quality candidates, defensible hiring process | **Medium** — Accountability for decisions influenced by AI |
| **Company (Employer)** | System owner | Efficiency, quality of hire, legal compliance, reputation | **High** — Legal liability, reputational risk, regulatory compliance |
| **Mugil Soft Solutions** | System developer (if building) | Responsible development, client trust, professional reputation | **Medium** — Professional accountability for system quality |

---

## 3. Risk Assessment

### 3.1 Identified Risks

| # | Risk | Description | Severity | Likelihood | Affected Stakeholders |
|---|------|-------------|----------|------------|----------------------|
| R1 | **Gender Bias** | Model trained on historical data may reproduce gender-based hiring patterns, disadvantaging women or non-binary candidates | Critical | Likely | Applicants, employer |
| R2 | **Age Discrimination** | Graduation dates, technology stack, and career length may serve as proxies for age | High | Possible | Older/younger applicants |
| R3 | **Ethnic/Racial Bias** | Historical hiring data may underrepresent certain ethnic groups, leading to biased rankings | Critical | Possible | Applicants from underrepresented groups |
| R4 | **Disability Discrimination** | CVs mentioning disability, career gaps due to health, or accessibility needs may be penalised | High | Possible | Applicants with disabilities |
| R5 | **Socioeconomic Bias** | Model may favour candidates from prestigious institutions or companies, disadvantaging those from less well-known backgrounds | Medium | Likely | Candidates from less privileged backgrounds |
| R6 | **Privacy Violation** | CVs contain extensive personal data (name, address, education history, employment history, sometimes health information, photographs) | High | Possible | All applicants |
| R7 | **Hallucination** | AI may misinterpret CV content, fabricate qualifications, or produce incorrect relevance assessments | High | Possible | Applicants (wrongly ranked), recruiters (misled) |
| R8 | **Opacity / Lack of Explanation** | Candidates and recruiters cannot understand why rankings are produced | High | Very Likely (if not designed) | Applicants, recruiters |
| R9 | **Exclusion** | Candidates with non-standard CV formats, multilingual CVs, or unconventional career paths may be systematically disadvantaged by the parsing algorithm | Medium | Likely | Candidates with non-traditional backgrounds |
| R10 | **Incorrect Recommendations** | Qualified candidates may be ranked low; unqualified candidates may be ranked high | High | Possible | Applicants, recruiters, employer |
| R11 | **Lack of Human Review** | Pressure to automate may erode the human-in-the-loop design over time | High | Possible | Applicants, employer |
| R12 | **Automation Bias** | Recruiters may accept AI rankings without critical evaluation | Medium | Likely | Applicants, recruiters |
| R13 | **Model Drift** | System accuracy may degrade over time as job markets, skill requirements, and applicant populations change | Medium | Likely | All stakeholders |
| R14 | **Adversarial Manipulation** | Candidates may learn to optimise CVs for the AI rather than genuinely representing their qualifications | Medium | Possible | Employer, other applicants |

---

## 4. Framework Evaluation

### 4.1 DPDP Act, 2023 (India)

**Applicability:** Directly applicable if the system processes personal data of Indian data principals (job applicants in India).

| Requirement | Assessment | Status |
|-------------|-----------|--------|
| **Personal Data Identification** | CVs contain extensive personal data: name, contact details, address, education, employment history, potentially photographs and health-related information | Must be addressed |
| **Lawful Processing Basis** | Consent is the most likely basis — applicants must be informed that AI will assist in screening and must consent to this processing | Must be implemented |
| **Purpose Limitation** | Data collected for recruitment must not be used for other purposes (e.g., marketing, profiling, AI model training without separate consent) | Must be enforced |
| **Data Minimisation** | Only CV data necessary for the screening purpose should be processed — photographs, addresses, and other unnecessary fields should be excluded from AI processing | Must be implemented |
| **Data Principal Rights** | Applicants must be able to access information about processing, request correction, and request erasure | Must be implemented |
| **Children's Data** | If interns or apprentices under 18 may apply, additional protections (verifiable parental consent) are required | Must be assessed |
| **Data Retention** | CV data must not be retained beyond the recruitment cycle unless separate consent is obtained | Must be enforced |
| **Security Safeguards** | Appropriate security measures (encryption, access controls) must be in place for CV data | Must be implemented |
| **Breach Notification** | Process for notifying the Data Protection Board and affected applicants in case of data breach | Must be implemented |

**Overall DPDP Assessment:** The system requires comprehensive privacy controls. A DPDP + AI Checklist (Portfolio Asset 04) should be completed before deployment.

---

### 4.2 NIST AI Risk Management Framework (AI RMF)

**Applicability:** Voluntary but highly recommended as the operational risk management framework.

| NIST Function | Application to AI Hiring Tool | Status |
|---------------|------------------------------|--------|
| **GOVERN** | Establish governance structure: accountability owner, risk classification (High), approval workflow, policies for AI-assisted hiring, incident reporting | Must be implemented |
| **MAP** | Identify context: hiring domain, affected people (applicants), intended use (advisory ranking), stakeholders, legal requirements, societal impact, known limitations | Must be documented |
| **MEASURE** | Assess risks: bias testing across demographic groups, accuracy evaluation, fairness metrics, reliability testing, adversarial testing, privacy assessment | Must be conducted |
| **MANAGE** | Act on risks: implement controls (debiasing, human oversight, appeal process), allocate resources, define response plans, monitor deployed system, communicate residual risks | Must be implemented |

**Trustworthy AI Characteristics Assessment:**

| Characteristic | Assessment |
|---------------|------------|
| Valid and Reliable | Must demonstrate consistent accuracy on representative test data |
| Safe | Must not cause harm through incorrect rejections or biased rankings |
| Secure and Resilient | Must resist adversarial CV manipulation and protect against data breaches |
| Accountable and Transparent | Must assign clear ownership and provide explanations for rankings |
| Explainable and Interpretable | Must provide meaningful reasons for candidate rankings |
| Privacy-Enhanced | Must implement data minimisation, access controls, and consent |
| Fair with Harmful Bias Managed | Must test for and mitigate demographic bias; document residual risks |

**Overall NIST Assessment:** NIST AI RMF provides the most actionable framework for this system. All four functions (Govern, Map, Measure, Manage) must be operationalised.

---

### 4.3 OECD AI Principles

**Applicability:** As high-level principles, these inform the ethical direction of the project.

| OECD Principle | Application | Assessment |
|---------------|-------------|------------|
| **Inclusive Growth and Well-being** | The system should improve hiring efficiency without creating exclusionary barriers. It should expand opportunity, not narrow it. | Risk: system may narrow opportunity if biased. Control: bias testing, diverse data, appeal process |
| **Human-Centred Values and Fairness** | The system must respect applicants' rights, dignity, and autonomy. It must not discriminate unfairly. | Risk: discrimination, loss of autonomy. Control: fairness audits, human oversight, transparency |
| **Transparency and Explainability** | Applicants should know AI is used. Recruiters should understand why candidates are ranked. | Risk: opacity. Control: AI disclosure, explainable rankings, model documentation |
| **Robustness, Security, and Safety** | The system should perform reliably and securely, with traceability and risk management. | Risk: model drift, adversarial manipulation, security breaches. Control: monitoring, security testing, adversarial testing |
| **Accountability** | Clear responsibility for the system's design, deployment, and outcomes must be established. | Risk: diffused responsibility. Control: designated owner, audit trails, incident reporting |

**Overall OECD Assessment:** The principles are well-aligned with the controls already identified. They reinforce the need for fairness, transparency, and accountability.

---

### 4.4 UNESCO Recommendation on the Ethics of AI

**Applicability:** Provides the ethical foundation, particularly regarding human rights, dignity, and non-discrimination.

| UNESCO Value/Principle | Application | Assessment |
|----------------------|-------------|------------|
| **Human Rights and Dignity** | The right to work and non-discrimination in employment are fundamental human rights. AI screening must not undermine these rights. | Critical concern: any bias in the system directly threatens these rights |
| **Fairness and Non-Discrimination** | The system must not discriminate on the basis of gender, age, race, disability, or other protected characteristics. | Requires rigorous bias testing and ongoing monitoring |
| **Transparency and Explainability** | UNESCO emphasises that people should be informed when AI affects them and should be able to understand the basis of AI-influenced decisions. | Requires AI disclosure and candidate-facing explanations |
| **Human Oversight and Determination** | UNESCO holds that humans should retain ultimate authority over significant decisions. AI should assist, not replace, human judgement. | Design as advisory tool with mandatory human decision-making is well-aligned |
| **Privacy and Data Protection** | UNESCO calls for respect for privacy rights and data protection in AI systems. | Requires privacy controls as identified in the DPDP assessment |
| **Proportionality and Do No Harm** | The use of AI must be proportionate to the purpose. If the risks outweigh the benefits, AI should not be used. | Must demonstrate that efficiency gains do not come at the cost of fairness |

**Overall UNESCO Assessment:** The ethical framework reinforces the critical importance of non-discrimination, transparency, and human oversight in AI-assisted hiring.

---

### 4.5 EU AI Act

**Applicability:** Directly applicable if the system is deployed within the EU or offered to EU-based employers. Also serves as a global best-practice benchmark.

**Risk Classification:** AI systems used in **recruitment and selection of candidates** are explicitly classified as **High-Risk AI systems** under the EU AI Act (Annex III, Section 4).

| EU AI Act Requirement | Application | Status |
|----------------------|-------------|--------|
| **Risk Management System** | Implement a risk management system throughout the AI lifecycle, including risk identification, assessment, mitigation, and monitoring | Must be implemented |
| **Data Governance** | Training, validation, and testing datasets must be relevant, representative, and as error-free as possible. Examination for biases that may lead to discrimination. | Must be implemented — current training data has identified representativeness issues |
| **Technical Documentation** | Comprehensive documentation of the system's design, purpose, capabilities, limitations, testing, and performance | Must be created |
| **Record-Keeping (Logging)** | Automatic recording of events (logs) for traceability of system functioning | Must be implemented |
| **Transparency** | Provide clear information about the AI system to deployers (employers), including capabilities, limitations, and instructions for use | Must be provided |
| **Human Oversight** | Designed to be effectively overseen by humans. Deployers must ensure human oversight of the system during use. | Designed as advisory tool — must be enforced operationally |
| **Accuracy, Robustness, Cybersecurity** | Achieve appropriate levels of accuracy, robustness, and resilience against errors, faults, and attacks | Must be demonstrated through testing |
| **Quality Management System** | Implement a quality management system covering risk management, data governance, testing, monitoring, and incident management | Must be established |
| **Conformity Assessment** | Self-assessment of conformity before market placement (for most high-risk AI in hiring) | Must be conducted before deployment (if deploying in EU) |
| **EU Database Registration** | Registration in the EU database for high-risk AI systems | Required before deployment in EU |
| **Post-Market Monitoring** | Establish and document a post-market monitoring system | Must be implemented |
| **Serious Incident Reporting** | Report serious incidents to relevant national authorities | Procedure must be established |

**Penalties for Non-Compliance:**
- Up to €15 million or 3% of global annual turnover for high-risk AI violations
- Up to €35 million or 7% of global annual turnover for prohibited AI practices

**Overall EU AI Act Assessment:** The AI hiring tool falls squarely within the EU AI Act's high-risk category. Full compliance is required for EU market deployment. Even for non-EU deployment, EU AI Act requirements serve as a robust governance benchmark.

---

## 5. Proposed Controls

### 5.1 Fairness Controls

| # | Control | Implementation | Verification |
|---|---------|---------------|--------------|
| F1 | **Representative Training Data** | Rebalance training data to better reflect the applicant population across gender, age, ethnicity, and other dimensions | Data audit report showing demographic distribution |
| F2 | **Bias Testing** | Test model outputs for disparate impact across gender, age, and ethnicity using gender-swapped and name-swapped CV pairs | Bias test results with statistical significance analysis |
| F3 | **Feature Review** | Remove or neutralise features that serve as proxies for protected characteristics (e.g., names, photographs, graduation dates) | Feature list review documentation |
| F4 | **Bias Mitigation** | Apply debiasing techniques (pre-processing, in-processing, or post-processing) if disparate impact is identified | Mitigation technique documentation, before/after comparison |
| F5 | **Ongoing Monitoring** | Monitor ranking distributions by demographic group post-deployment with alert thresholds | Monitoring dashboard, alert configuration |
| F6 | **Periodic Re-Audit** | Conduct bias audit quarterly for the first year, then semi-annually | Scheduled audit calendar, audit reports |

### 5.2 Transparency Controls

| # | Control | Implementation | Verification |
|---|---------|---------------|--------------|
| T1 | **AI Disclosure** | Inform all applicants that AI assists in the screening process, during the application process | Disclosure text in application form/process |
| T2 | **Recruiter Explanations** | Provide recruiters with explanations of why each candidate was ranked (feature importance, qualification match) | Explanation output samples, recruiter feedback |
| T3 | **Candidate Explanations** | Provide rejected candidates with a summary of key factors upon request | Candidate communication templates, explanation mechanism |
| T4 | **System Documentation** | Create and maintain a model card documenting intended use, training data, performance, limitations, and bias testing results | Model card document |

### 5.3 Privacy Controls

| # | Control | Implementation | Verification |
|---|---------|---------------|--------------|
| P1 | **Consent** | Obtain informed consent from applicants for AI-assisted screening. Provide option for human-only review. | Consent mechanism, consent records |
| P2 | **Data Minimisation** | Process only the CV fields necessary for qualification matching. Exclude photographs, addresses, and other unnecessary data. | Data field inventory, processing scope documentation |
| P3 | **Access Controls** | Restrict access to CV data to authorised personnel only. Implement role-based access controls. | Access control configuration, access audit logs |
| P4 | **Encryption** | Encrypt CV data at rest and in transit | Encryption configuration documentation |
| P5 | **Retention Policy** | Retain CV data only for the duration of the recruitment cycle plus legally required period. Automated deletion thereafter. | Retention policy, deletion automation evidence |
| P6 | **DPDP Compliance** | Complete the DPDP + AI Checklist for this system (if processing data of Indian data principals) | Completed DPDP checklist |

### 5.4 Human Oversight Controls

| # | Control | Implementation | Verification |
|---|---------|---------------|--------------|
| HO1 | **Advisory Only** | AI output is explicitly positioned as advisory — final decisions are made by human recruiters and hiring managers | System design documentation, user interface labelling |
| HO2 | **Override Capability** | Recruiters can adjust, override, or ignore AI rankings. Overrides are logged. | Override mechanism testing, override log samples |
| HO3 | **Recruiter Training** | All recruiters using the system complete training on AI limitations, bias awareness, and when to override | Training materials, completion records |
| HO4 | **Anti-Automation-Bias Measures** | AI rankings presented as one input among many. System does not auto-reject candidates. Recruiters encouraged to review low-ranked candidates. | UI design review, recruiter feedback |
| HO5 | **Periodic Human Audit** | Sample of AI-recommended shortlists reviewed by senior recruiters or HR managers for quality and fairness | Audit schedule, sample review reports |

### 5.5 Accountability Controls

| # | Control | Implementation | Verification |
|---|---------|---------------|--------------|
| A1 | **Accountability Owner** | Designated senior manager accountable for the AI hiring system's governance, performance, and compliance | Named owner in governance documentation |
| A2 | **Audit Trail** | Comprehensive logging of AI inputs (anonymised), outputs, model version, recruiter actions, and overrides | Log samples, retention policy |
| A3 | **Appeal Process** | Formal process for candidates to request human review of AI-influenced decisions. Contact information provided in rejection communications. | Appeal process documentation, candidate communication |
| A4 | **Incident Reporting** | Defined process for reporting and investigating AI incidents (incorrect rankings, bias complaints, data issues) | Incident reporting procedure, incident log |
| A5 | **Governance Review** | Quarterly governance review of system performance, incident history, bias metrics, and compliance status | Governance review schedule, review reports |

### 5.6 Documentation and Monitoring Controls

| # | Control | Implementation | Verification |
|---|---------|---------------|--------------|
| D1 | **Model Card** | Document system purpose, training data, performance metrics, limitations, bias testing results, and maintenance schedule | Model card document |
| D2 | **Risk Register** | Maintain a dedicated risk register for this system (see Section 3) with quarterly updates | Risk register, update history |
| D3 | **Performance Monitoring** | Real-time monitoring of accuracy, error rates, and ranking distributions | Monitoring dashboard |
| D4 | **Drift Detection** | Monitor for model drift and data drift indicators; trigger retraining or re-evaluation when thresholds are exceeded | Drift detection configuration, alert logs |
| D5 | **Regulatory Tracking** | Monitor for changes in applicable regulations (DPDP Act rules, EU AI Act implementation, employment law) | Regulatory review schedule |

---

## 6. Governance Gate Assessment

Applying Mugil Soft Solutions' AI Governance Gate:

| Gate Step | Assessment | Pass/Fail |
|-----------|-----------|-----------|
| Purpose identified | Yes — assist recruiters in CV screening and candidate ranking | ✅ |
| Users identified | Yes — recruiters, hiring managers | ✅ |
| Affected people identified | Yes — job applicants | ✅ |
| Data identified | Yes — CVs (personal data), job specifications | ✅ |
| Personal data identified | Yes — extensive personal data in CVs | ✅ |
| Risks identified | Yes — 14 risks identified (see Section 3) | ✅ |
| Fairness assessed | Assessed — bias risks identified, controls proposed | ⚠️ Requires implementation |
| Transparency assessed | Assessed — disclosure and explanation controls proposed | ⚠️ Requires implementation |
| Accountability assessed | Assessed — owner and audit controls proposed | ⚠️ Requires implementation |
| Privacy assessed | Assessed — DPDP and privacy controls proposed | ⚠️ Requires implementation |
| Human oversight assessed | Assessed — advisory-only design with override capability | ⚠️ Requires testing |
| Controls determined | Yes — 28 controls across 6 categories (see Section 5) | ✅ |
| Testing conducted | Partially — preliminary testing shows gender bias; full testing required | ❌ Not yet complete |
| Documentation complete | Partially — this governance review exists; model card and full docs needed | ❌ Not yet complete |
| Human approval | Not yet — founder approval required for high-risk deployment | ❌ Pending |
| Deployment | Not yet — blocked pending controls and approval | ❌ Blocked |
| Monitoring ready | Designed but not implemented | ❌ Not yet implemented |
| Incident management ready | Process defined but not tested | ⚠️ Requires testing |

**Gate Decision: DEPLOYMENT NOT APPROVED**

The AI hiring tool must not be deployed until:
1. ❌ All "Immediate" priority controls are implemented
2. ❌ Full bias testing is completed with acceptable results
3. ❌ Privacy controls are verified
4. ❌ Documentation is complete (model card, risk register, test results)
5. ❌ Monitoring is operational
6. ❌ Founder provides explicit written approval

---

## 7. Conclusion

This governance review demonstrates that AI-assisted hiring is a **high-risk application** that requires comprehensive governance controls. The system has legitimate business value — reducing screening time and improving consistency — but this value must not come at the expense of fairness, privacy, or transparency.

### What This Case Study Shows

1. **AI governance is not optional for high-risk AI** — Multiple global frameworks (EU AI Act, NIST, OECD, UNESCO) and India's DPDP Act converge on the need for rigorous controls
2. **Bias is a real and measurable risk** — Preliminary testing identified gender-based disparate impact, validating the need for systematic testing
3. **Affected people must be considered** — Job applicants are directly and significantly affected by this system; their rights to transparency, fairness, and appeal are paramount
4. **Human oversight is essential** — The system must remain advisory, with qualified human decision-makers retaining authority
5. **Governance is an ongoing responsibility** — Deployment is not the end; monitoring, re-auditing, and incident management are continuous obligations

### Recommendations

| Priority | Action |
|----------|--------|
| **Immediate** | Rebalance training data and re-test for disparate impact |
| **Immediate** | Implement candidate AI disclosure and appeal process |
| **Before Deployment** | Complete all bias, privacy, and security testing |
| **Before Deployment** | Create model card and complete governance documentation |
| **Before Deployment** | Train recruiters on AI-assisted hiring |
| **Before Deployment** | Obtain founder approval through AI Governance Gate |
| **Post-Deployment** | Activate monitoring and establish quarterly governance review |

---

*Version 1.0 — Mugil Soft Solutions*
*This governance review is for professional and educational purposes. It does not constitute legal advice. Where legal compliance is critical, engage qualified legal professionals. Framework details are based on publicly available source documents.*
