# AI Bias Audit

**Mugil Soft Solutions — Portfolio Asset | Week 6**

> A structured bias and fairness audit for AI systems. This document provides a template with a worked example — an AI-assisted hiring tool — demonstrating how to evaluate data representativeness, outcome fairness, transparency, human oversight, appeal mechanisms, and documentation.

---

## Important Note on Language

This audit uses **evidence-based language**. We do not claim that any AI system is "bias-free." Instead, we use terms such as:

- **Tested** — The area was actively evaluated
- **Observed** — A specific finding was identified through testing
- **Identified** — A risk or issue was found
- **Not identified in available testing** — No issue was found in the tests conducted, but this does not guarantee absence
- **Requires further testing** — Additional evaluation is needed to reach a conclusion

---

## Audit Scope

| Field | Detail |
|-------|--------|
| **AI System** | AI-Assisted CV Screening and Candidate Ranking Tool |
| **System Purpose** | Screen incoming CVs, extract qualifications and experience, and rank candidates by relevance to a job specification |
| **Users** | Recruiters, hiring managers |
| **Affected People** | Job applicants (including those who may be unfairly rejected or ranked) |
| **Audit Date** | [Date] |
| **Auditor** | Mugil Soft Solutions — AI Governance Team |
| **Audit Type** | Pre-deployment fairness review |

---

## Audit Summary

| Audit Area | Overall Finding | Risk Level | Priority |
|------------|----------------|------------|----------|
| Data Representativeness | Issues identified — training data underrepresents certain demographic groups | High | Immediate |
| Outcome Fairness | Disparate impact observed in preliminary testing for gender | High | Immediate |
| Transparency | Partial — feature importance available but no candidate-facing explanation | Medium | Before deployment |
| Human Oversight | Designed but not yet tested in practice | Medium | Before deployment |
| Appeal Mechanism | Not yet implemented | High | Before deployment |
| Documentation | Partial — technical documentation exists but governance documentation incomplete | Medium | Before deployment |

---

## Detailed Audit

### 1. Data Representativeness

| # | Question | Finding | Evidence | Risk | Control |
|---|----------|---------|----------|------|---------|
| 1.1 | Is the training data representative of the population the AI system will serve? | **Issue identified.** The training dataset is composed of 73% male and 27% female CVs, reflecting historical hiring patterns rather than the applicant population. Age distribution skews towards 25–40 years. Ethnic diversity data is not captured. | Training data demographic analysis report (n=15,000 CVs). Gender inferred from names and pronouns. Age inferred from graduation dates. | High — The model may learn to favour profiles resembling the majority training group (male, 25–40). | Rebalance training data to better reflect the expected applicant population. Where rebalancing is not feasible, apply bias mitigation techniques during model training. Collect anonymised demographic metadata for ongoing monitoring. |
| 1.2 | Does the training data contain labels or annotations that may embed historical bias? | **Issue identified.** Training labels are based on historical hire/no-hire decisions, which themselves may reflect human biases in past recruitment. | Labelling methodology documentation. Labels derived from recruiter decisions in 2019–2023 hiring cycles. | High — The model will learn to replicate historical hiring biases, including any discrimination present in past decisions. | Consider using task-completion or qualification-match labels instead of historical hire/no-hire. If historical labels are used, audit them for patterns of bias. |
| 1.3 | Are there underrepresented groups in the training data? | **Observed.** Several groups are underrepresented: applicants over 50 (2.1% of dataset), applicants with disclosed disabilities (0.3%), and applicants from certain geographic regions. | Demographic distribution analysis of training dataset. | Medium — The model may have lower accuracy or unfamiliar patterns for underrepresented groups, leading to unreliable rankings. | Augment training data for underrepresented groups where feasible. Test model performance specifically on underrepresented group samples. Document known gaps. |
| 1.4 | Is the data collection process itself potentially biased? | **Observed.** CVs were collected from a single job board and internal referrals, which may not represent the full applicant market. Referral-based CVs tend to mirror the demographics of existing employees. | Data source documentation. 40% of CVs sourced from internal referrals. | Medium — Source bias limits the diversity of the training data before any model is trained. | Diversify data sources. Include CVs from multiple job boards, university career services, and diversity-focused recruitment channels. |

---

### 2. Outcome Fairness

| # | Question | Finding | Evidence | Risk | Control |
|---|----------|---------|----------|------|---------|
| 2.1 | Could particular groups be systematically disadvantaged by the AI's outputs? | **Observed.** In preliminary testing, female-associated CVs received lower average ranking scores than male-associated CVs with equivalent qualifications (mean score difference: 0.15 on a 0–1 scale). | A/B testing with gender-swapped CV pairs (n=500 pairs). Statistical significance: p < 0.01. | High — Systematic gender-based disparate impact in candidate rankings. | Implement bias mitigation (debiasing techniques, adversarial training, or post-processing calibration). Retest after mitigation. Do not deploy until disparate impact is reduced to acceptable levels. |
| 2.2 | Are outcome metrics disaggregated by relevant demographic groups? | **Partially implemented.** Accuracy and ranking quality are tracked overall but not disaggregated by gender, age, or other demographic dimensions. | Model evaluation report. Overall precision: 0.82. No demographic breakdown. | Medium — Aggregate metrics can mask disparate performance across groups. | Implement disaggregated evaluation metrics by gender, age group, and other relevant dimensions. Report group-level performance alongside overall metrics. |
| 2.3 | Has the system been tested with adversarial or edge-case inputs? | **Not yet tested.** No adversarial testing or red teaming has been conducted on the hiring model. | Absence of adversarial testing report. | Medium — The model may behave unpredictably on unusual inputs (e.g., unconventional CV formats, multilingual CVs, non-traditional career paths). | Conduct adversarial testing before deployment, including unconventional CV formats, career gaps, non-traditional backgrounds, and multilingual inputs. |
| 2.4 | Are there mechanisms to detect outcome bias after deployment? | **Not yet implemented.** No post-deployment monitoring for demographic disparate impact is in place. | Absence of monitoring dashboard or reporting mechanism. | High — Bias may emerge or worsen after deployment as the applicant population or model behaviour drifts. | Implement ongoing monitoring of ranking distributions by demographic group. Set alert thresholds for disparate impact. Schedule quarterly bias reviews. |

---

### 3. Transparency

| # | Question | Finding | Evidence | Risk | Control |
|---|----------|---------|----------|------|---------|
| 3.1 | Can the AI's ranking decision be explained to a recruiter? | **Partially.** The system provides feature importance scores (e.g., "experience match: 0.7, skills match: 0.8, education match: 0.5") but does not provide natural language explanations. | Feature importance output samples from 20 test CVs. | Low-Medium — Recruiters may not interpret numerical feature weights correctly. | Add natural language explanation layer (e.g., "This candidate ranked highly because of strong match in required skills and relevant industry experience"). |
| 3.2 | Can the AI's decision be explained to a candidate? | **Not implemented.** No candidate-facing explanation is available. Candidates receive only accept/reject communication from the recruiter. | Review of candidate communication templates. | High — Candidates cannot understand why they were ranked low or rejected, preventing meaningful appeal. | Design candidate-facing explanation that communicates key factors in understandable language. Include in rejection communications. |
| 3.3 | Are candidates informed that AI is used in the screening process? | **Not yet implemented.** No disclosure mechanism exists. | Review of application process and candidate communications. | High — Candidates are unaware that AI influences their application outcome, preventing informed consent and undermining trust. | Add clear disclosure in the application process (e.g., "Your application will be initially assessed with the assistance of an AI screening tool. A human recruiter reviews all shortlisting decisions."). |

---

### 4. Human Oversight

| # | Question | Finding | Evidence | Risk | Control |
|---|----------|---------|----------|------|---------|
| 4.1 | Can a human override the AI's ranking? | **Designed but not tested.** The system design allows recruiters to manually adjust rankings, but this capability has not been tested with actual recruiters. | System design documentation showing manual override feature. | Low (if working) — But untested controls provide no assurance. | Conduct user acceptance testing with recruiters. Verify that overrides are logged and that the system does not revert overrides. |
| 4.2 | Is there a human-in-the-loop before final hiring decisions? | **Yes.** The system is designed as a ranking assistant — final shortlisting and hiring decisions are made by human recruiters and hiring managers. | Process flow documentation showing AI output feeds into human decision-making. | Low — The human-in-the-loop design is appropriate. | Ensure this design is maintained and not eroded over time (e.g., by pressure to "automate more"). Monitor override rates as an indicator of AI-human agreement and engagement. |
| 4.3 | Are recruiters trained to critically evaluate AI rankings rather than blindly accepting them? | **Not yet implemented.** No recruiter training programme for AI-assisted hiring exists. | Absence of training materials or training records. | Medium — Without training, recruiters may develop automation bias, accepting AI rankings without independent evaluation. | Develop and deliver recruiter training covering: AI limitations, common bias patterns, when to override, how to document overrides. |

---

### 5. Appeal Mechanism

| # | Question | Finding | Evidence | Risk | Control |
|---|----------|---------|----------|------|---------|
| 5.1 | Can affected people (candidates) challenge the AI's influence on their application? | **Not implemented.** No formal appeal process exists for candidates who believe the AI screening was unfair. | Review of candidate communication and complaints processes. | High — Without an appeal mechanism, candidates who are unfairly disadvantaged have no recourse. This is both an ethical failure and a potential legal risk. | Implement a formal appeal process. Inform candidates of their right to request human review. Designate a point of contact for AI-related complaints. |
| 5.2 | Is the appeal process accessible and clearly communicated? | **Not applicable** — no appeal process exists to evaluate. | N/A | High — Even if an appeal process is created, it must be communicated clearly and be genuinely accessible. | Include appeal information in rejection communications. Provide multiple contact channels. Set and communicate response timelines. |
| 5.3 | Are appeal outcomes tracked and used to improve the system? | **Not applicable** — no appeal process exists to evaluate. | N/A | Medium — Without feedback from appeals, the organisation loses a valuable signal for identifying and correcting bias. | Track appeal volume, outcomes, and patterns. Feed appeal findings back into model evaluation and retraining processes. |

---

### 6. Documentation

| # | Question | Finding | Evidence | Risk | Control |
|---|----------|---------|----------|------|---------|
| 6.1 | Is the AI system's design, training data, and evaluation adequately documented? | **Partially.** Technical documentation exists (model architecture, training parameters, evaluation metrics) but governance documentation (risk assessment, bias testing, approval records) is incomplete. | Technical design document (v2.1). Governance documentation gaps identified in this audit. | Medium — Incomplete documentation hinders accountability, auditability, and incident investigation. | Complete governance documentation including: risk register, bias test results, data audit, approval records, monitoring plan. Maintain version-controlled documentation. |
| 6.2 | Are audit trails maintained for AI-influenced decisions? | **Partially.** The system logs AI ranking scores but does not log the full input features, model version, or recruiter actions (accept/override/reject). | System logging specification review. | Medium — Incomplete audit trails prevent post-hoc analysis of decisions and hinder incident investigation. | Extend logging to capture: model version, input features used, ranking score, recruiter action (accept/override), override reason (if provided). Retain logs for the legally required retention period. |
| 6.3 | Is there a model card or system card documenting the AI's capabilities and limitations? | **Not implemented.** No model card or system card exists. | Absence of model card documentation. | Low-Medium — Without a model card, stakeholders cannot quickly understand the system's intended use, limitations, and known issues. | Create a model card documenting: intended use, training data summary, evaluation results, known limitations, bias test results, and maintenance schedule. |

---

## Audit Recommendations Summary

| Priority | Recommendation | Risk Addressed |
|----------|---------------|----------------|
| **Immediate** | Rebalance training data and retest for gender disparate impact before deployment | Gender bias, data representativeness |
| **Immediate** | Implement candidate-facing AI disclosure in the application process | Transparency, consent |
| **Immediate** | Design and implement candidate appeal process | Fairness, accountability |
| **Before Deployment** | Complete governance documentation (risk register, bias test results, approval records) | Documentation, accountability |
| **Before Deployment** | Implement disaggregated evaluation metrics by demographic group | Outcome fairness monitoring |
| **Before Deployment** | Develop and deliver recruiter training on AI-assisted hiring | Automation bias, human oversight |
| **Before Deployment** | Add natural language explanations for AI rankings | Transparency, explainability |
| **Post-Deployment** | Implement ongoing bias monitoring with alert thresholds | Drift, emerging bias |
| **Post-Deployment** | Create model card and maintain version-controlled documentation | Documentation, auditability |

---

## Audit Conclusion

This pre-deployment bias audit has identified **several significant issues** that must be addressed before the AI-assisted hiring tool is deployed:

1. **Training data underrepresents women and older applicants**, creating a risk of biased model behaviour
2. **Gender-based disparate impact was observed** in preliminary testing
3. **No candidate-facing transparency or appeal mechanism** exists
4. **Recruiter training on AI limitations** has not been developed

These findings are **not unusual for an early-stage AI system** and are addressable through the controls recommended above. The audit recommends that **deployment should not proceed** until the "Immediate" priority items are resolved and evidence of mitigation effectiveness is documented.

---

*Version 1.0 — Mugil Soft Solutions*
*This audit is for professional and educational purposes. Bias audit findings should be validated by domain experts. This document does not constitute legal advice.*
