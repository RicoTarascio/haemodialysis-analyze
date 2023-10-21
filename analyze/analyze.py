import os
import sys
from pathlib import Path
from typing import List
import pandas as pd

from .utils import Utils
import pprint
import datetime
import json


class InvalidPatientFileException(Exception):
    def __init__(self, file_path, type):
        self.file = file_path
        self.type = type
        if type == "NOT_FOUND":
            super().__init__(
                "[ERROR]: Patient file was not found in path: " + str(file_path)
            )
        elif type == "INVALID_TYPE":
            super().__init__(
                "[ERROR]: Patient file is not an excel file (.xlsx or .xls)."
            )
        else:
            super().__init__("[ERROR]: Invalid patient file.")


class Analyze:
    @staticmethod
    def analyze(patient_file_path: str | os.DirEntry[str], parameters: dict):
        if not os.path.exists(patient_file_path):
            raise InvalidPatientFileException(patient_file_path, "NOT_FOUND")
        if not Utils.is_file_valid(patient_file_path):
            raise InvalidPatientFileException(patient_file_path, "INVALID_TYPE")

        errors = []

        file = pd.ExcelFile(patient_file_path)

        patient_name = Utils.find_patient_name(file)
        months = [month for month in file.sheet_names if month in Utils.MONTHS]
        # TODO: Data di nascita

        patient_reads = Utils.patient_reads(file, months)
        out_of_range = Analyze.get_out_of_range(patient_reads, parameters)

        if patient_name is None:
            pprint.pprint("NAME IS MISSING")
            errors.append("NAME")

        if len(months) != 12:
            pprint.pprint(str(len(months) - 12) + " MONTHS ARE MISSING")
            errors.append("MONTHS")

        if len(out_of_range) > 0:
            pprint.pprint("SOME READS ARE OUT OF RANGE")
            errors.append("OUT_OF_RANGE")

        if len(errors) > 0:
            pprint.pprint("THERE ARE ERRORS")
            # TODO: report_errors(path) -> creates and stores CSV with patient errors
            return

        # TODO: At this point it should save CV with patient info

        patient_data = {
            "name": patient_name,
            "file": str(patient_file_path),
            "birth": "",
            "acquisition_date": datetime.datetime.today().isoformat(),
            "reads": patient_reads,
        }

        return patient_data

    @staticmethod
    def get_out_of_range(patient_reads: dict, parameters: dict):
        out_of_range: List[List] = []
        for month, dates in patient_reads.items():
            for day, values in dates.items():
                for param, ranges in parameters.items():
                    read = values.get(param)
                    if read == None:
                        # Parameter value was not found
                        continue
                    read_val = float(read)
                    if read_val < ranges[0] or read_val > ranges[1]:
                        out_of_range.append(
                            [month, day, param, ranges[0], ranges[1], read_val]
                        )
        return out_of_range

    @staticmethod
    def out_of_range_to_cv(out_of_range: List[List], path: str | Path):
        df = pd.DataFrame(
            out_of_range,
            columns=["Mese", "Giorno", "Parametro", "Minimo", "Massimo", "Valore"],
        )

        if not os.path.exists(path):
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(path, index_label=None, index=False)
        return

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

    @staticmethod
    def patient_data_to_json(patient_data: dict):
        return json.dumps(patient_data)
