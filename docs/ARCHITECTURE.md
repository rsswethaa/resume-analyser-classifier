# Architecture

```mermaid
sequenceDiagram
  participant R as Resume
  participant J as Job Description
  participant P as Preprocessor
  participant B as S-BERT
  participant A as Analyser
  R->>P: candidate text
  J->>P: role text
  P->>B: cleaned texts
  B-->>A: semantic embeddings
  A->>A: cosine similarity + skill coverage
  A-->>R: score, match class, missing skills
```

`SBERTEncoder` is a lazy wrapper around `sentence-transformers`. Unit tests use the deterministic lexical path to avoid network/model downloads in CI; semantic similarity can be supplied from S-BERT during a full run.
