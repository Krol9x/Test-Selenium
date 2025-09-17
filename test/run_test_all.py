# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 02:57:44 2025

@author: huber
"""

import os
import pytest

def main():

    test_folder = os.path.abspath(os.path.dirname(__file__))

    test_files = [
        "test_app_ui.py",
        "portfolio_test.py",
        "link_test.py",
        "language_test.py",
        "profile_test.py",
        "skill_test.py",
        "edu_test.py",
        "contact_test.py",
        "exp_test.py",
        "courses_test.py",
        "home_test.py",
    ]

    test_paths = [os.path.join(test_folder, f) for f in test_files]
    exit_code = pytest.main(test_paths + ["-v"])
    return exit_code

if __name__ == "__main__":
    code = main()
    exit(code)