import io
import tempfile
import unittest
from pathlib import Path

import app as product_app
from src.document_parser import extract_text
from src.product_analyser import analyse_candidate, extract_sections, rank_candidates


class ResumeProductTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        product_app.app.config.update(TESTING=True, DATABASE=str(Path(self.tmp.name) / 'resume.db'))
        self.client = product_app.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_txt_parser(self):
        self.assertEqual(extract_text('resume.txt', b'Python and SQL'), 'Python and SQL')

    def test_section_extraction(self):
        sections = extract_sections('Skills\nPython SQL\nExperience\nAnalyst 2022-2024\nProjects\nDashboard')
        self.assertIn('Python', sections['skills'])
        self.assertIn('Analyst', sections['experience'])
        self.assertIn('Dashboard', sections['projects'])

    def test_section_aware_analysis_explains_gaps(self):
        result = analyse_candidate('Skills\nPython SQL\nExperience\nData analyst 2022-2024', 'Need Python SQL Tableau and data analysis', use_sbert=False)
        self.assertIn('python', result['matched_skills'])
        self.assertIn('tableau', result['missing_skills'])
        self.assertIn('experience', result['sections_found'])
        self.assertEqual(result['explanation']['protected_attributes_used'], [])

    def test_rank_candidates(self):
        candidates = [
            {'candidate':'A','analysis':{'score':40}},
            {'candidate':'B','analysis':{'score':80}},
        ]
        ranked = rank_candidates(candidates)
        self.assertEqual(ranked[0]['candidate'], 'B')
        self.assertEqual(ranked[0]['rank'], 1)

    def test_multi_candidate_upload_api(self):
        job = 'Data Analyst role requiring Python SQL Tableau data analysis and communication.'
        data = {
            'job_title':'Data Analyst',
            'job_description':job,
            'resumes':[
                (io.BytesIO(b'Skills\nPython SQL Tableau data analysis communication\nExperience\nAnalyst 2022-2025'), 'strong.txt'),
                (io.BytesIO(b'Skills\nExcel communication\nExperience\nAdministrator 2024-2025'), 'other.txt'),
            ],
        }
        response = self.client.post('/api/compare', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(len(payload['candidates']), 2)
        self.assertEqual(payload['candidates'][0]['candidate'], 'Strong')
        self.assertEqual(payload['audit']['protected_attributes_used'], [])

    def test_health(self):
        self.assertEqual(self.client.get('/health').get_json()['status'], 'ok')


if __name__ == '__main__':
    unittest.main()
