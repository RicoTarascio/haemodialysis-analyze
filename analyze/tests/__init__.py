import datetime
import sys
from ..analyze import Analyze
from ..utils import Utils
from ..patient import Patient
import os
import cProfile
from pathlib import Path 

ROOT_DIR = os.path.abspath(os.curdir)
ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original")
PARAMETERS_PATH = os.path.join(ROOT_DIR, "analyze/tests/ranges.xlsx")
TEST_OUT_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/out")

def full_test(test_one: bool = False):
    if not os.path.exists(ORIGINAL_FOLDER_PATH):
        print(
            "[WARNING]: Original files folder was not found, one will be created for you in ./original."
        )
        os.makedirs(ORIGINAL_FOLDER_PATH, exist_ok=True)

    if not os.path.exists(TEST_OUT_FOLDER_PATH):
        print(
            "[WARNING]: Tests out folder was not found, one will be created for you."
        )
        os.makedirs(TEST_OUT_FOLDER_PATH, exist_ok=True)

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
        name = p.name if p.name is not None else ""
        csv_path = Path(TEST_OUT_FOLDER_PATH, "".join(["_".join(name.split(" ")), "_", str(datetime.datetime.today().year), ".csv"]))
        r.save_to_csv(csv_path)
        if test_one: return r
        reports.append(r) 
    return reports



cProfile.runctx('full_test(True)', None, locals()) # type: ignore


