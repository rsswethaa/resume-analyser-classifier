import unittest
from src.analyser import analyse_resume
from src.text_utils import extract_skills, cosine_similarity

class ResumeAnalyserTests(unittest.TestCase):
    def test_skill_extraction(self):
        skills = extract_skills("Python and SQL with Power BI")
        self.assertIn("python", skills)
        self.assertIn("sql", skills)
        self.assertIn("power bi", skills)

    def test_strong_match_scores_higher(self):
        job = "Python SQL data analysis communication"
        strong = analyse_resume("Python SQL data analysis communication", job)
        weak = analyse_resume("graphic design photography", job)
        self.assertGreater(strong["score"], weak["score"])

    def test_semantic_override(self):
        result = analyse_resume("finance analyst", "financial analyst", semantic_similarity=0.9)
        self.assertGreater(result["score"], 50)

    def test_cosine(self):
        self.assertAlmostEqual(cosine_similarity([1,0],[1,0]), 1.0)

if __name__ == "__main__":
    unittest.main()
