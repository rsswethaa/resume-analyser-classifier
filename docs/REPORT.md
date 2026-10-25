# Technical Project Report — Resume Analyser & Classifier

## Executive summary
This project demonstrates a complete NLP resume-analysis workflow combining semantic similarity, explicit skill extraction, versioned match scoring, SQLite persistence and human-review-oriented auditability.

## 1. Problem
Keyword-only screening can miss relevant experience when candidates and job descriptions use different wording, while opaque automated ranking can create fairness and accountability risks.

## 2. Objective
Build a hybrid semantic/skill matching pipeline that remains explainable, testable and auditable.

## 3. NLP method
The full integration uses Sentence-BERT (`sentence-transformers/all-MiniLM-L6-v2`) to create dense resume/job vectors and cosine similarity for semantic alignment. Explicit skill extraction provides interpretable overlap. CI uses a deterministic lexical fallback to avoid network/model-download dependence.

## 4. Data architecture
Resumes and job descriptions are stored separately. Skills use a normalised catalogue with many-to-many links. Each match stores semantic score, skill score, final score, classification and exact encoder version. Audit events track creation and scoring actions.

## 5. Testing
Automated tests validate preprocessing/scoring plus end-to-end SQLite match/audit persistence. CI compiles and runs tests on each change.

## 6. Responsible AI
No autonomous rejection or hiring recommendation should rely solely on this score. Real use requires validated job-related criteria, fairness testing, accessibility, privacy/retention controls, candidate rights and human oversight.

## 7. Security/privacy
Resumes can contain sensitive personal data. Production deployment requires restricted access, encryption, safe document parsing, audit logs and defined deletion policies.

## 8. Limitations
Semantic similarity is not performance prediction. No hiring-outcome validity, calibrated probability, fairness certification or legal compliance claim is made.

## 9. Future work
Section-aware parsing, education/experience extraction, multilingual embeddings, recruiter-reviewed evaluation sets, calibrated role taxonomies, fairness metrics and human-in-the-loop explanations.

## Conclusion
The repository now contains working NLP code, a real database/audit layer, SQL assets, ER/data-flow diagrams, tests, CI, deployment/security docs, model documentation and a formal technical report.
