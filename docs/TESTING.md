# Testing Strategy

Automated tests cover cleaning, skill extraction, cosine similarity, deterministic fallback scoring, match classification and SQLite persistence/audit events.

Run:
```bash
python -m unittest discover -s tests -v
```

CI intentionally avoids downloading S-BERT weights. Local S-BERT can be enabled with `requirements-ml.txt`.

Future evaluation should include recruiter-reviewed relevance sets, multilingual cases, section-aware resumes, accessibility/format variation, subgroup fairness analysis and calibration of score bands.
