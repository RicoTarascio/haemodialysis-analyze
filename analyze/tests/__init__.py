import sys
from ..analyze import Analyze
from ..utils import Utils
import os
import cProfile
import pprint
from ..utils import Utils


def test_files():
    if not os.path.exists(Utils.ORIGINAL_FOLDER_PATH):
        print(
            "[WARNING]: Original files folder was not found, one will be created for you in ./original."
        )
        os.makedirs(Utils.ORIGINAL_FOLDER_PATH, exist_ok=True)

    if not os.path.exists(Utils.TEST_OUT_FOLDER_PATH):
        print("[WARNING]: Tests out folder was not found, one will be created for you.")
        os.makedirs(Utils.TEST_OUT_FOLDER_PATH, exist_ok=True)

    if not os.path.exists(Utils.PARAMETERS_PATH):
        sys.exit(
            "[ERROR]: Parameters file was not found in path: " + Utils.PARAMETERS_PATH
        )

    if not Utils.is_file_valid(Utils.PARAMETERS_PATH):
        sys.exit("[ERROR]: Parameters file is not an excel file (.xlsx or .xls).")

    original_dir = Utils.get_dir(Utils.ORIGINAL_FOLDER_PATH)
    valid_files = list(filter(Utils.is_file_valid, original_dir))

    return valid_files


def full_test(test_one: bool = False, test_pattern: str | None = None):
    parameters = Analyze.to_parameters(Utils.PARAMETERS_PATH)
    valid_files = test_files()

    for f in valid_files:
        if test_pattern and not f.path.endswith(test_pattern):
            continue
        pprint.pprint("Analyzing: " + f.path)
        patient_data = Analyze.analyze(f.path, parameters)
        pprint.pprint("OK")
        pprint.pprint("==================================")
        if patient_data is not None:
            pprint.pprint(patient_data)

        if test_one:
            return


# cProfile.runctx("full_test()", None, locals())  # type: ignore

full_test()
