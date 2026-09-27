# AI Governance Glossary

**Mugil Soft Solutions — Portfolio Asset | Week 1**

> A practical glossary of essential AI governance terms. Each term includes a simple definition, a business example, an AI-specific example, and why it matters. Designed for professionals entering the AI governance space.

---

## 1. AI Governance

**Definition:** The set of policies, processes, controls, and accountability structures that guide how an organisation develops, deploys, and manages AI systems.

**Business Example:** A company creates a review board that must approve all AI projects before deployment — this board is part of AI governance.

**AI Example:** An AI-powered loan approval system has documented policies specifying who can modify the model, how it is tested for fairness, and what happens if it produces incorrect decisions.

**Why It Matters:** Without governance, AI systems can be deployed without oversight, leading to uncontrolled risks, reputational damage, and regulatory exposure.

---

## 2. Responsible AI

**Definition:** The practice of designing, developing, and deploying AI systems in a manner that is ethical, fair, transparent, accountable, and respectful of human rights and privacy.

**Business Example:** A recruitment platform commits to testing its AI screening tool for gender and age bias before using it to evaluate candidates.

**AI Example:** An AI chatbot that handles customer complaints is designed to escalate complex or sensitive cases to a human agent rather than making autonomous decisions.

**Why It Matters:** Responsible AI builds trust with customers, reduces legal risk, and differentiates companies that take AI ethics seriously from those that do not.

---

## 3. AI Risk

**Definition:** The potential for an AI system to cause harm — whether to individuals, groups, organisations, or society — through incorrect outputs, biased decisions, privacy violations, or other failures.

**Business Example:** A retail company's AI demand forecasting model consistently overestimates demand for certain regions, leading to costly excess inventory.

**AI Example:** A medical diagnosis AI misclassifies a serious condition as benign, delaying treatment for a patient.

**Why It Matters:** Identifying and managing AI risks before deployment prevents harm, financial loss, and erosion of public trust.

---

## 4. Bias (AI Bias)

**Definition:** A systematic and unfair skew in an AI system's outputs that disadvantages particular groups of people, often arising from biased training data, flawed model design, or unrepresentative evaluation.

**Business Example:** An AI-powered hiring tool trained primarily on CVs from male applicants learns to penalise CVs that mention women's colleges or women's sports teams.

**AI Example:** A facial recognition system has significantly lower accuracy for people with darker skin tones because the training dataset was predominantly composed of lighter-skinned faces.

**Why It Matters:** AI bias can perpetuate and amplify existing societal inequalities, cause direct harm to individuals, and expose organisations to legal and reputational risk.

---

## 5. Fairness

**Definition:** The principle that AI systems should produce equitable outcomes and should not discriminate against individuals or groups based on protected characteristics such as race, gender, age, disability, or religion.

**Business Example:** A bank's AI credit scoring system is audited to verify that applicants from different ethnic backgrounds receive comparable approval rates when their financial profiles are similar.

**AI Example:** An AI content moderation tool is tested to ensure it does not disproportionately flag content in certain languages or dialects as harmful.

**Why It Matters:** Fairness is both a moral imperative and increasingly a legal requirement. Unfair AI systems erode trust and can result in regulatory penalties.

---

## 6. Transparency

**Definition:** The practice of making the existence, purpose, capabilities, limitations, and decision-making processes of an AI system understandable and accessible to relevant stakeholders.

**Business Example:** An insurance company informs customers that their claim is being assessed with AI assistance and explains what factors influence the decision.

**AI Example:** A chatbot clearly identifies itself as an AI system at the start of every conversation rather than pretending to be a human.

**Why It Matters:** Transparency enables informed consent, builds user trust, and is required by multiple regulatory frameworks including the EU AI Act.

---

## 7. Accountability

**Definition:** The assignment of clear ownership and responsibility for an AI system's design, deployment, behaviour, outcomes, and impact — ensuring that humans remain answerable for AI-driven decisions.

**Business Example:** A company designates a senior manager as the accountable owner for an AI customer service system, responsible for reviewing its performance and handling complaints.

**AI Example:** When an autonomous AI agent makes an incorrect purchase recommendation that causes a customer financial loss, the company — not the AI — is held responsible.

**Why It Matters:** Without accountability, no one owns the consequences of AI failures, making it impossible to remediate harm or improve systems.

---

## 8. Explainability

**Definition:** The ability to describe how an AI system reaches a specific output or decision in terms that relevant stakeholders can understand.

**Business Example:** A loan applicant is told that their application was declined primarily because their debt-to-income ratio exceeded the threshold, not simply told "the algorithm decided."

**AI Example:** A medical AI provides a confidence score and highlights the specific image features that led to a diagnostic suggestion, allowing the physician to validate the reasoning.

**Why It Matters:** Explainability supports trust, enables human oversight, and is essential for appeal processes and regulatory compliance.

---

## 9. Privacy

**Definition:** The right of individuals to control how their personal data is collected, used, stored, and shared — and the obligation of organisations to protect that data.

**Business Example:** A healthcare app collects only the patient data necessary for its stated purpose and does not share it with advertisers.

**AI Example:** An AI model is trained on anonymised data rather than raw personal records, and the trained model cannot be reverse-engineered to reveal individual data points.

**Why It Matters:** Privacy violations cause direct harm to individuals, breach regulations such as India's DPDP Act 2023 and Europe's GDPR, and destroy customer trust.

---

## 10. Consent

**Definition:** The informed, voluntary agreement of an individual to the collection, processing, or use of their personal data for a specified purpose.

**Business Example:** A mobile app asks users to explicitly opt-in before using their location data for personalised recommendations.

**AI Example:** A job applicant is informed that an AI system will assist in screening their CV and is given the choice to consent or to request a purely human review.

**Why It Matters:** Consent is a foundational requirement under most data protection laws and is essential for ethical data use in AI systems.

---

## 11. Data Minimisation

**Definition:** The principle that organisations should collect and process only the minimum amount of personal data necessary to achieve a specific, stated purpose.

**Business Example:** A customer feedback system collects the feedback text and a satisfaction rating — it does not also collect the customer's home address or date of birth.

**AI Example:** An AI sentiment analysis system processes only the text of customer reviews, not the reviewers' names, email addresses, or purchase histories.

**Why It Matters:** Collecting unnecessary data increases privacy risk, storage costs, and the potential impact of a data breach — with no corresponding benefit.

---

## 12. Human Oversight

**Definition:** The design and operation of AI systems such that qualified humans can monitor, review, intervene in, or override AI-driven decisions — particularly for high-impact or high-risk use cases.

**Business Example:** A content moderation AI flags posts for review, but a human moderator makes the final decision on whether to remove content.

**AI Example:** An AI diagnostic tool presents its findings to a physician who reviews the recommendation and makes the clinical decision — the AI does not act autonomously.

**Why It Matters:** Human oversight prevents automation failures from causing unchecked harm and is required by most AI governance frameworks for high-risk applications.

---

## 13. AI Incident

**Definition:** An event in which an AI system causes or contributes to harm, produces unintended consequences, fails in an unexpected way, or behaves outside its intended parameters.

**Business Example:** An AI pricing algorithm unexpectedly sets prices at near-zero for several hours due to a data pipeline error, causing significant financial loss.

**AI Example:** A conversational AI begins generating offensive or harmful responses after encountering adversarial inputs that exploit prompt injection vulnerabilities.

**Why It Matters:** Incident identification, reporting, and analysis are essential for learning from failures, improving systems, and maintaining stakeholder trust.

---

## 14. AI Monitoring

**Definition:** The continuous or periodic observation and measurement of an AI system's performance, behaviour, outputs, and impact after deployment.

**Business Example:** A company tracks its AI recommendation system's click-through rate, error rate, and customer complaint rate on a weekly dashboard.

**AI Example:** An AI fraud detection system is monitored for model drift — the gradual decline in accuracy as transaction patterns change over time.

**Why It Matters:** AI systems can degrade, drift, or develop new failure modes after deployment. Without monitoring, these issues go undetected until they cause harm.

---

## 15. AI Policy

**Definition:** A formal organisational document that defines the rules, principles, approved uses, restricted uses, and governance processes for AI within the organisation.

**Business Example:** A company's AI policy states that AI may not be used to make autonomous decisions about employee termination without human review.

**AI Example:** An AI policy specifies that all LLM-based applications must include a disclaimer informing users that responses are AI-generated and may contain errors.

**Why It Matters:** Policies convert governance principles into enforceable organisational standards, ensuring consistent and responsible AI use.

---

## 16. Impact Assessment (AI Impact Assessment)

**Definition:** A structured evaluation process that identifies and analyses the potential effects of an AI system on individuals, groups, and society — conducted before or during deployment.

**Business Example:** Before launching an AI-powered loan decision system, a bank assesses the potential impact on applicants from different demographic groups.

**AI Example:** An AI impact assessment for a facial recognition system evaluates accuracy across ethnic groups, identifies surveillance risks, and proposes mitigation measures.

**Why It Matters:** Impact assessments surface risks early, inform governance decisions, and demonstrate due diligence to regulators and stakeholders.

---

## 17. Red Teaming (AI Red Teaming)

**Definition:** The practice of deliberately testing an AI system by attempting to make it fail, produce harmful outputs, leak data, or behave unexpectedly — in order to identify vulnerabilities before deployment.

**Business Example:** Before launching a customer-facing chatbot, a team of testers deliberately inputs offensive, misleading, and manipulative prompts to see how the system responds.

**AI Example:** Security researchers attempt prompt injection attacks against an LLM-based application to determine whether they can extract confidential system instructions or bypass safety filters.

**Why It Matters:** Red teaming reveals vulnerabilities that standard testing misses, enabling proactive risk mitigation before real users encounter problems.

---

## 18. Reliability

**Definition:** The ability of an AI system to perform its intended function consistently and correctly under expected operating conditions over time.

**Business Example:** A customer support AI provides accurate answers 95% of the time during normal business hours and maintains the same accuracy during peak demand.

**AI Example:** A machine translation system produces consistent quality across different document types and does not intermittently produce nonsensical translations.

**Why It Matters:** Unreliable AI systems erode user trust, increase support costs, and can cause direct harm when users depend on them for important decisions.

---

## 19. Safety

**Definition:** The property of an AI system that ensures it does not cause physical, psychological, financial, or societal harm to individuals or groups — whether through intended operation or failure.

**Business Example:** An autonomous warehouse robot has emergency stop mechanisms and collision avoidance to prevent injuries to warehouse workers.

**AI Example:** A mental health chatbot is designed to detect crisis language (e.g., expressions of self-harm) and immediately connect the user to a human professional rather than continuing the AI conversation.

**Why It Matters:** Safety failures in AI systems can cause irreversible harm. Safety-by-design is a non-negotiable requirement for responsible deployment.

---

## 20. Hallucination

**Definition:** The generation of outputs by an AI system — particularly large language models — that are fluent and plausible-sounding but factually incorrect, fabricated, or unsupported by any source material.

**Business Example:** An AI legal research assistant confidently cites a court case that does not exist, leading a lawyer to include a fabricated citation in a court filing.

**AI Example:** A RAG-based customer support system answers a question about product return policies by generating a policy that sounds reasonable but does not match the company's actual return policy.

**Why It Matters:** Hallucinations undermine the trustworthiness of AI systems. In high-stakes domains (legal, medical, financial), they can cause direct harm and legal liability.

---

## 21. Automation Bias

**Definition:** The tendency of humans to over-rely on AI system outputs, accepting AI recommendations without sufficient critical evaluation — even when the AI output is incorrect.

**Business Example:** A doctor accepts an AI diagnostic suggestion without performing their own clinical evaluation because "the AI is usually right."

**AI Example:** A recruiter automatically rejects candidates flagged by an AI screening tool without reviewing the underlying reasoning or considering that the AI may be biased.

**Why It Matters:** Automation bias converts AI errors into human decisions, defeating the purpose of human oversight and increasing the risk of harm.

---

## 22. Model Drift

**Definition:** The gradual degradation of an AI model's performance over time as the real-world data it encounters diverges from the data it was trained on.

**Business Example:** A fraud detection model trained on 2023 transaction patterns becomes less effective as new fraud techniques emerge in 2025.

**AI Example:** A sentiment analysis model trained on pre-pandemic customer feedback misinterprets the tone and language of post-pandemic communications.

**Why It Matters:** Model drift means that an AI system that worked well at deployment can silently become unreliable. Continuous monitoring is essential to detect and address drift.

---

## 23. Data Quality

**Definition:** The degree to which data used to train, evaluate, or operate an AI system is accurate, complete, consistent, timely, and representative of the real-world domain it is intended to model.

**Business Example:** A customer database with 30% missing email addresses and inconsistent name formatting produces an AI segmentation model that misclassifies customer groups.

**AI Example:** A medical imaging AI trained on a dataset that predominantly contains images from one scanner model performs poorly on images from other manufacturers.

**Why It Matters:** AI systems are only as good as their data. Poor data quality is one of the most common root causes of AI failure, bias, and unreliable outputs.

---

*Version 1.0 — Mugil Soft Solutions*
*This glossary is for professional and educational purposes. It does not constitute legal advice.*
