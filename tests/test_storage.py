import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.storage import add_job, add_resume, attach_skills, init_db, save_match


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / 'resume.db'
        init_db(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_match_audit_flow(self):
        resume = add_resume(self.db, 'C1', 'Python SQL data analyst')
        job = add_job(self.db, 'J1', 'Analyst', 'Python and SQL analyst role')
        attach_skills(self.db, 'resume', resume, ['python','sql'])
        attach_skills(self.db, 'job', job, ['python','sql'])
        save_match(self.db, resume, job, 0.82, 1.0, 88.0, 'STRONG_MATCH', 'lexical-fallback-v1')
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM matches').fetchone()[0], 1)
            self.assertGreaterEqual(db.execute('SELECT COUNT(*) FROM audit_events').fetchone()[0], 3)

    def test_empty_resume_rejected(self):
        with self.assertRaises(ValueError):
            add_resume(self.db, 'EMPTY', '  ')


if __name__ == '__main__':
    unittest.main()
