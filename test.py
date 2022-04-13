#!/bin/env python3
# -*- coding: utf8 -*- 

import subprocess
import unittest

from dotenv import load_dotenv
from pathlib import Path

# load testing configuration
load_dotenv(".env.test")

def run(command):
    result = subprocess.run(command, capture_output=True)
    return result

class TestRun(unittest.TestCase):
    def test_run_make_command(self):
        result = run(["poetry", "run", "python", "backup.py", "make"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity --verb 2 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics --exclude-filelist {Path.home()}/.backup/include --exclude ** {Path.home()} scp://localhost/backup\n")

    def test_run_make_code(self):
        result = run(["poetry", "run", "python", "backup.py", "make"])
        self.assertEqual(result.returncode, 0)

    def test_run_make_full_command(self):
        result = run(["poetry", "run", "python", "backup.py", "make", "--full"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity full --verb 2 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics --exclude-filelist {Path.home()}/.backup/include --exclude ** {Path.home()} scp://localhost/backup\n/usr/bin/duplicity remove-older-than 60d --force --verb 0 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup\n/usr/bin/duplicity cleanup --force --extra-clean --verb 0 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup\n")

    def test_run_make_full_code(self):
        result = run(["poetry", "run", "python", "backup.py", "make", "--full"])
        self.assertEqual(result.returncode, 0)

    def test_run_list_code(self):
        result = run(["poetry", "run", "python", "backup.py", "list"])
        self.assertEqual(result.returncode, 0)

    def test_run_list_command(self):
        result = run(["poetry", "run", "python", "backup.py", "list"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity collection-status --verb 0 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup\n")

    def test_run_content_code(self):
        result = run(["poetry", "run", "python", "backup.py", "content"])
        self.assertEqual(result.returncode, 0)

    def test_run_content_command(self):
        result = run(["poetry", "run", "python", "backup.py", "content"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity list-current-files --verb 0 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup\n")

    def test_run_content_date_code(self):
        result = run(["poetry", "run", "python", "backup.py", "content", "--date", "2022-01-01 23:00"])
        self.assertEqual(result.returncode, 0)

    def test_run_content_date_command(self):
        result = run(["poetry", "run", "python", "backup.py", "content", "--date", "2022-01-01 23:00"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity list-current-files --time 2022-01-01T230000 --verb 0 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup\n")

    def test_run_restore_code(self):
        result = run(["poetry", "run", "python", "backup.py", "restore", "--path", str(Path.home()) + "/backup-test"])
        self.assertEqual(result.returncode, 0)

    def test_run_restore_command(self):
        result = run(["poetry", "run", "python", "backup.py", "restore", "--path", str(Path.home()) + "/backup-test"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity --verb 0 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup /Users/piotr/backup-test\n")

    def test_run_restore_date_code(self):
        result = run(["poetry", "run", "python", "backup.py", "restore", "--date", "2022-01-01 23:00", "--path", str(Path.home()) + "/backup-test"])
        self.assertEqual(result.returncode, 0)

    def test_run_restore_date_command(self):
        result = run(["poetry", "run", "python", "backup.py", "restore", "--date", "2022-01-01 23:00", "--path", str(Path.home()) + "/backup-test"])
        self.assertEqual(result.stdout.decode('UTF-8'), f"/usr/bin/duplicity --verb 0 --time 2022-01-01T230000 --log-file ~/.backup/duplicity.log --asynchronous-upload --no-print-statistics scp://localhost/backup /Users/piotr/backup-test\n")

    def test_missing_path(self):
        result = run(["poetry", "run", "python", "backup.py", "restore", "--date", "2022-01-01 23:00"])
        self.assertEqual(result.returncode, 55)

if __name__ == "__main__":
    unittest.main()