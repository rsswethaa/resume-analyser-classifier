# Technical Report

## Problem
Keyword-only resume screening can miss semantically relevant experience when candidate wording differs from job-description wording.

## Objective
Demonstrate a hybrid resume-analysis pipeline combining semantic similarity with explicit skill coverage.

## S-BERT method
The full integration uses Sentence-BERT via `sentence-transformers/all-MiniLM-L6-v2` to encode resume and job-description text into dense vectors. Cosine similarity measures semantic alignment. A skill-extraction layer provides additional explainability.

## Lightweight reproducibility
CI avoids downloading model weights. Tests exercise cleaning, skill extraction, cosine similarity and scoring using a deterministic lexical fallback. The S-BERT wrapper can be enabled locally with `requirements-ml.txt`.

## Responsible-use boundary
No autonomous rejection or hiring recommendation should be based solely on this score. Production recruitment systems need job-related validation, bias/fairness testing, accessibility support, human review, consent, retention controls and legal review.

## Future work
Section-aware parsing, education/experience extraction, calibrated role taxonomies, multilingual embeddings, recruiter feedback loops, fairness evaluation and human-in-the-loop explanations.
