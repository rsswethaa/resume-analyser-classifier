import ipaddress, re, socket
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from flask import Blueprint, jsonify, request

class TextExtractor(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data):
        text=' '.join(data.split())
        if text: self.parts.append(text)
    def text(self): return '\n'.join(self.parts)

def _public_host(host):
    for addr in socket.getaddrinfo(host,None):
        ip=ipaddress.ip_address(addr[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast: return False
    return True

def import_job_post(url):
    parsed=urlparse(url)
    if parsed.scheme not in {'http','https'} or not parsed.hostname: raise ValueError('A public http(s) URL is required')
    if not _public_host(parsed.hostname): raise ValueError('Private or local network addresses are blocked')
    req=Request(url,headers={'User-Agent':'ResumeAnalyserPortfolio/1.0'})
    with urlopen(req,timeout=8) as resp:
        kind=(resp.headers.get_content_type() or '').lower()
        if kind not in {'text/html','text/plain'}: raise ValueError('URL must return HTML or plain text')
        raw=resp.read(1_000_001)
    if len(raw)>1_000_000: raise ValueError('Job page is too large')
    text=raw.decode('utf-8','ignore')
    if kind=='text/html':
        parser=TextExtractor(); parser.feed(text); text=parser.text()
    text=re.sub(r'\n{3,}','\n\n',text).strip()
    if len(text)<50: raise ValueError('No useful job text found')
    return text[:50000]

def register_advanced(app):
    bp=Blueprint('resume_advanced',__name__)
    @bp.post('/api/job/import')
    def job_import():
        payload=request.get_json(silent=True) or {}
        try: text=import_job_post(str(payload.get('url','')).strip())
        except Exception as exc: return jsonify({'error':str(exc)}),400
        return jsonify({'job_description':text,'characters':len(text),'note':'Public-page import only; site terms and robots rules remain the user’s responsibility.'})
    app.register_blueprint(bp)
