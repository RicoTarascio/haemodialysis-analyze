from ..analyze import Analyze
import os

ROOT_DIR = os.path.abspath(os.curdir)
ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original")
PARAMETERS_PATH = os.path.join(ROOT_DIR, "analyze/tests/ranges.xlsx")

anal = Analyze(ORIGINAL_FOLDER_PATH, PARAMETERS_PATH)

f1 = anal.patients_files[0]

for month in f1.sheet_names:
    if month not in ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]:
        continue
    df = anal.read_patient_data(f1, month)
    anal.analyze_patient(df, month)
