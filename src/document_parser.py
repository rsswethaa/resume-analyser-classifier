from io import BytesIO
from pathlib import Path


def extract_text(filename: str, data: bytes) -> str:
    """Extract text from TXT, PDF or DOCX bytes."""
    suffix = Path(filename).suffix.lower()
    if suffix in {'.txt', '.md'}:
        return data.decode('utf-8', errors='ignore').strip()
    if suffix == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(data))
        return '\n'.join((page.extract_text() or '') for page in reader.pages).strip()
    if suffix == '.docx':
        from docx import Document
        document = Document(BytesIO(data))
        return '\n'.join(p.text for p in document.paragraphs if p.text.strip()).strip()
    raise ValueError('Supported resume formats are PDF, DOCX and TXT')
