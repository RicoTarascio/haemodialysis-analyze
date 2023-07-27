import pandas as pd
import os, sys

ROOT_DIR = os.path.abspath(os.curdir)
DEFAULT_ORIG_FOLDER_PATH = os.path.join(ROOT_DIR, "original")
class Analyze:
    original_folder_path: str
    patients_files: list[os.DirEntry]
    parameters = []
    
    def __init__(self, original_folder_path: str, parameters_file_path: str) -> None:
        if not os.path.exists(original_folder_path):
            print(
                "[WARNING]: Original files folder was not found, one will be created for you in ./original."
            )
            os.makedirs(DEFAULT_ORIG_FOLDER_PATH, exist_ok=True)

        
        if not os.path.exists(parameters_file_path):
            sys.exit("[ERROR]: Parameters file was not found in path: " + parameters_file_path)
        
        if not Analyze.is_file_valid(parameters_file_path):
            sys.exit("[ERROR]: Parameters file is not an excel file (.xlsx or .xls).")

        self.parameters = Analyze.read_parameters(parameters_file_path)

        original_dir = Analyze.get_dir(original_folder_path)
        valid_files = list(filter(Analyze.is_file_valid, original_dir))

        self.original_folder_path = original_folder_path
        self.patients_files = valid_files

        self.analyze_patient(self.patients_files[0])


    @staticmethod
    def read_patient_data(patient_file: os.DirEntry, sheet_name: str | None, params_to_filter: dict | None):
        df = pd.read_excel(patient_file, sheet_name=sheet_name, index_col=0, header=2)
        df.drop_duplicates(inplace=True)
        df = df.filter(axis='index', items=params_to_filter.keys())
        df = df.filter(regex='([1-9])+-\w{3}$', axis='columns')
        return df
    
    @staticmethod
    def get_month_dates(dates_raw):
        dates = []
        pre = 0
        for x in dates_raw:
            x = str(x)
            if x.find("-") > -1:
                if int(x.split("-")[0]) > pre:
                    dates.append(x.split("-")[0])
                    pre = int(x.split("-")[0])
                else: break
        return dates
    
    def analyze_patient(self, patient_file: os.DirEntry):
        f = pd.ExcelFile(patient_file)
        print("\n\n")
        for month in f.sheet_names:
            if month not in ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]:
                    continue
            print("MONTH: " + month)
            patient_data = Analyze.read_patient_data(f, month, self.parameters)
            dates = patient_data.columns
            params = patient_data.index

            raw_data = patient_data.to_numpy()

            for p_i, p_row in enumerate(raw_data):
                print(params[p_i])
                for r_i, r in enumerate(p_row):
                    print(dates[r_i], r)
                print("\n\n")
            print("\n\n\n")
        return ""

    @staticmethod
    def read_parameters(parameters_file_path: str): 
        df = pd.read_excel(parameters_file_path)
        full_read = df.to_numpy()
        parameters = {x[0]: [x[1], x[2]] for x in full_read if not pd.isna(x[0]) and not pd.isna(x[1]) and not pd.isna(x[2])}

        return parameters

    @staticmethod
    def get_dir(path: str):
        return list(os.scandir(path))
    
    @staticmethod
    def is_file_valid(file: os.DirEntry | str):
        if isinstance(file, os.DirEntry):
            if str(file.name).find(".xlxs") == -1 and str(file.name).find(".xls") == -1:
                return False
            return True
        if file.find(".xlxs") == -1 and file.find(".xls") == -1:
            return False
        return True
    


