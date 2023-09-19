import os
import sys
from .utils import Utils
import pandas as pd
import json
import datetime


class Patient:
    name: str | None = ""
    month_reads: list = []
    file: pd.ExcelFile
    data: str

    def __init__(self, file_path: str | os.DirEntry[str]) -> None:
        self.set_file(file_path)

    def set_file(self, file_path: str | os.DirEntry[str]):
        if not os.path.exists(file_path):
            sys.exit("[ERROR]: Patient file was not found in path: " + str(file_path))

        if not Utils.is_file_valid(file_path):
            sys.exit("[ERROR]: Patient file is not an excel file (.xlsx or .xls).")

        self.file = pd.ExcelFile(file_path)
        self.name = Utils.find_patient_name(self.file)
        self.month_reads = [
            month
            for month in self.file.sheet_names
            if month
            in [
                "Gennaio",
                "Febbraio",
                "Marzo",
                "Aprile",
                "Maggio",
                "Giugno",
                "Luglio",
                "Agosto",
                "Settembre",
                "Ottobre",
                "Novembre",
                "Dicembre",
            ]
        ]

        if len(self.month_reads) != 12:
            sys.exit("[ERROR]: Patient excel file does not contain all months")

        patient_data = {
            "patient": self.name,
            "file": str(file_path),
            "acquisition_date": datetime.datetime.today().isoformat(),
            "data": {},
        }

        for sheet_name in self.month_reads:
            patient_data["data"][sheet_name] = json.loads(
                Utils.to_json(self.file, sheet_name)
            )

        self.data = json.dumps(patient_data)
        print(self.data)
