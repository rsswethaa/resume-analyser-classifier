# Security, Privacy and Hiring-Use Boundary

## Status

Resume Analyser & Classifier is a portfolio decision-support prototype. It is not an autonomous hiring authority and should not be used to automatically reject or select candidates.

## Sensitive data

Resumes can contain personal information. The public demo should be used only with synthetic, redacted or non-sensitive example resumes.

Do not commit or upload to GitHub issues:

- real candidate resumes without permission
- addresses, phone numbers or personal identifiers
- API keys, database passwords or cloud credentials
- production hiring data

## Current boundary

- supported document inputs include PDF, DOCX and TXT
- scoring uses job-description similarity, skills/keywords and section-aware evidence
- protected demographic attributes are not intended scoring inputs
- excluding protected attributes does not by itself establish fairness
- model/version metadata is retained for auditability

## Production requirements

A real recruitment deployment would require:

- authenticated recruiters and role-based access
- tenant isolation and secure document storage
- malware/file-type/size validation for uploads
- retention and deletion controls
- CSRF protection and API authentication
- rate limiting and audit logging
- representative bias/outcome testing
- accessible alternatives
- legally validated job-related scoring criteria
- human review of every consequential decision

## Vulnerability reporting

Please do not disclose exploitable details or personal resume data in a public issue. Contact the repository owner privately through the GitHub profile with reproduction steps and the affected version.
