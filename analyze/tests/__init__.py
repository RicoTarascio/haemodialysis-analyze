from ..analyze import Analyze
import os

ROOT_DIR = os.path.abspath(os.curdir)
ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original")
PARAMETERS_PATH = os.path.join(ROOT_DIR, "analyze/tests/ranges.xlsx")

anal = Analyze(ORIGINAL_FOLDER_PATH, PARAMETERS_PATH)