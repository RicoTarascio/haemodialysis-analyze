from ..analyze import Analyze
import os

ROOT_DIR = os.path.abspath(os.curdir)
ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original")

anal = Analyze(ORIGINAL_FOLDER_PATH)