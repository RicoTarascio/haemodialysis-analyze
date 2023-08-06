import os
import sys
from pathlib import Path 
import pandas as pd

from .utils import Utils
from .patient import Patient


class Analyze:
    @staticmethod
    def analyze(patient: Patient, parameters: dict):
        report = PatientReport(patient)
        
        for month, df in patient.data.items():
            df = df.drop_duplicates()
            df = df.filter(axis='index', items=parameters.keys())
            dates = df.columns
            params = df.index

            raw_data = df.to_numpy()

            for p_i, p_row in enumerate(raw_data):
                for r_i, r in enumerate(p_row):
                    ranges = parameters[params[p_i]]
                    read_val = float(r)
                    
                    if read_val < ranges[0] or read_val > ranges[1]:
                        report.add_out_of_range(params[p_i], dates[r_i], read_val)
        return report

    @staticmethod
    def to_parameters(parameters_file_path: str): 
        df = pd.read_excel(parameters_file_path)
        full_read = df.to_numpy()
        parameters = {x[0]: [x[1], x[2]] for x in full_read if not pd.isna(x[0]) and not pd.isna(x[1]) and not pd.isna(x[2])}

        return parameters
    

class PatientReport:
    patient: Patient
    out_of_ranges: dict = dict()

    def __init__(self, patient: Patient) -> None:
        self.patient = patient
        
    def add_out_of_range(self, param: str, date: str, value: float):

        if self.out_of_ranges.get(date) is None:
            self.out_of_ranges[date] = dict()
            self.out_of_ranges[date][param] = value
            return
        self.out_of_ranges[date][param] = value

    def save_to_csv(self, path: str | Path):
        df = pd.DataFrame(self.out_of_ranges)
        if(not os.path.exists(path)):             
            path = Path(path)  
            path.parent.mkdir(parents=True, exist_ok=True)  
        df.to_csv(path) 
        return
    


