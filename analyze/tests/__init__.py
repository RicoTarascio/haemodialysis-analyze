import sys
from ..analyze import Analyze
from ..utils import Utils
from ..patient import Patient
import os
import cProfile

ROOT_DIR = os.path.abspath(os.curdir)
ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original")
PARAMETERS_PATH = os.path.join(ROOT_DIR, "analyze/tests/ranges.xlsx")

def full_test():
    if not os.path.exists(ORIGINAL_FOLDER_PATH):
        print(
            "[WARNING]: Original files folder was not found, one will be created for you in ./original."
        )
        os.makedirs(ORIGINAL_FOLDER_PATH, exist_ok=True)


    if not os.path.exists(PARAMETERS_PATH):
        sys.exit("[ERROR]: Parameters file was not found in path: " + PARAMETERS_PATH)

    if not Utils.is_file_valid(PARAMETERS_PATH):
        sys.exit("[ERROR]: Parameters file is not an excel file (.xlsx or .xls).")

    parameters = Analyze.to_parameters(PARAMETERS_PATH)


    original_dir = Utils.get_dir(ORIGINAL_FOLDER_PATH)
    valid_files = list(filter(Utils.is_file_valid, original_dir))

    reports = []

    for f in valid_files:
        p = Patient(f)
        r = Analyze.analyze(p, parameters)
        reports.append(r) 


cProfile.runctx('full_test()', None, locals())


