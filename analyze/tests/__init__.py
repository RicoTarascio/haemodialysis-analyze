import sys
from ..analyze import Analyze
from ..utils import Utils
from ..patient import Patient
import os

ROOT_DIR = os.path.abspath(os.curdir)
ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original")
PARAMETERS_PATH = os.path.join(ROOT_DIR, "analyze/tests/ranges.xlsx")


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

f_p1 = valid_files[1]

p1 = Patient(f_p1)

report_p1 = Analyze.analyze(p1, parameters)

print(report_p1.out_of_ranges)