# Setup and Deployment

## Lightweight local demo
```bash
git clone https://github.com/rsswethaa/resume-analyser-classifier.git
cd resume-analyser-classifier
python demo.py
python -m unittest discover -s tests -v
```

## S-BERT
```bash
pip install -r requirements-ml.txt
```

## Optional database
```bash
python -c "from src.storage import init_db; init_db('resume_analyser.db', seed=True)"
```

A real service would separate document ingestion, parsing/embedding workers, model registry, encrypted document storage, access-controlled recruiter APIs and managed databases.
