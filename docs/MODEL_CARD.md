# Model Card — Hybrid Resume Matching Prototype

## Intended use
Educational semantic/skill matching between resume and job-description text.

## Components
- text preprocessing
- explicit skill extraction
- S-BERT (`all-MiniLM-L6-v2`) when installed
- deterministic lexical fallback for CI/demo
- cosine similarity plus skill overlap

## Output
Fit score and descriptive classification band.

## Limitations
Semantic similarity is not job performance prediction. Resume writing style, language, formatting and missing context can affect scores. S-BERT embeddings are not inherently fair or legally validated for hiring.

## Prohibited use
Autonomous rejection, protected-trait inference or unreviewed candidate ranking for consequential hiring decisions.
