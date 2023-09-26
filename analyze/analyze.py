import os
import sys
from pathlib import Path
from typing import Dict, Collection, List
import pandas as pd

from .utils import Utils
from .patient import Patient
import pprint


class Analyze:
    @staticmethod
    def analyze(patient: Patient, parameters: dict):
        report = PatientReport(patient)

        patient_reads = patient.patient_data["reads"]

        for month, dates in patient_reads.items():
            for day, values in dates.items():
                for param, ranges in parameters.items():
                    read = values.get(param)
                    if read == None:
                        # Parameter value was not found
                        continue
                    read_val = float(read)
                    if read_val < ranges[0] or read_val > ranges[1]:
                        report.add_out_of_range(
                            param_name=param,
                            param_min=ranges[0],
                            param_max=ranges[1],
                            day=day,
                            month=month,
                            value=read_val,
                        )

        return report

    @staticmethod
    def to_parameters(parameters_file_path: str):
        df = pd.read_excel(parameters_file_path)
        full_read = df.to_numpy()
        parameters = {
            x[0]: [x[1], x[2]]
            for x in full_read
            if not pd.isna(x[0]) and not pd.isna(x[1]) and not pd.isna(x[2])
        }

        return parameters


class PatientReport:
    patient: Patient
    out_of_ranges: List[List] = []

    def __init__(self, patient: Patient) -> None:
        self.patient = patient

    def add_out_of_range(
        self,
        param_name: str,
        param_min: float,
        param_max: float,
        month: str,
        day: str,
        value: float,
    ):
        self.out_of_ranges.append([month, day, param_name, param_min, param_max, value])

    def save_to_csv(self, path: str | Path):
        df = pd.DataFrame(
            self.out_of_ranges,
            columns=["Mese", "Giorno", "Parametro", "Minimo", "Massimo", "Valore"],
        )
        if not os.path.exists(path):
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index_label=None, index=False)
        return
