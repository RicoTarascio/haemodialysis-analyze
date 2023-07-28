import os
import sys
from .utils import Utils
import pandas as pd

class Patient:
    name: str = ""
    month_reads: list = []
    file: pd.ExcelFile
    data: dict()

    def __init__(self, file_path: str) -> None:
        self.set_file(file_path)
            
    
    def set_file(self, file_path: str):
        if not os.path.exists(file_path):
            sys.exit("[ERROR]: Patient file was not found in path: " + file_path)

        if not Utils.is_file_valid(file_path):
            sys.exit("[ERROR]: Patient file is not an excel file (.xlsx or .xls).")

        self.file = pd.ExcelFile(file_path)
        self.name = Utils.find_patient_name(self.file)
        self.month_reads = [month for month in self.file.sheet_names if month in ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]]
        self.data = Utils.get_patient_data(self.file)
        

    
    
