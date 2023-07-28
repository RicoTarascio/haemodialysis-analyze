import os
import sys
import pandas as pd

from .utils import Utils
from .patient import Patient


class Analyze:
    
    # @Returns - values for each month that are out of parameters range
    @staticmethod
    def analyze(patient: Patient, parameters: dict):
        report = PatientReport(patient, parameters)
        
        for month, df in patient.data.items():
            df = df.filter(axis='index', items=parameters.keys())
            dates = df.columns
            params = df.index

            raw_data = df.to_numpy()

            for p_i, p_row in enumerate(raw_data):
                for r_i, r in enumerate(p_row):
                    ranges = parameters[params[p_i]]
                    read_val = float(r)
                    
                    if read_val < ranges[0] or read_val > ranges[1]:
                        report.add_out_of_range(params[p_i], month, dates[r_i], read_val)
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

    def __init__(self, patient: Patient, params: dict) -> None:
        self.patient = patient
        for m in ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]:
            self.out_of_ranges[m] = dict()
        

    def add_out_of_range(self, param: str, month: str, date: str, value: str):
        if self.out_of_ranges.get(month) is None:
            print("MONTH NOT IN KEYS")
            return
        if(self.out_of_ranges[month].get(param) is None):
            self.out_of_ranges[month] = dict()
            self.out_of_ranges[month][param] = [[date, value]]
            return
        self.out_of_ranges[month][param].append([date, value]) 


    def save_to_file(path: str):
        return
    


