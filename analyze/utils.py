import os
import pandas as pd


class Utils:
    @staticmethod
    def get_dir(path: str):
        return list(os.scandir(path))
    
    @staticmethod 
    def to_excel(file: os.DirEntry):
        return pd.ExcelFile(file)
    
    @staticmethod
    def is_file_valid(file: os.DirEntry | str):
        if isinstance(file, os.DirEntry):
            if str(file.name).find(".xlxs") == -1 and str(file.name).find(".xls") == -1:
                return False
            return True
        if file.find(".xlxs") == -1 and file.find(".xls") == -1:
            return False
        return True
    
    @staticmethod
    def find_patient_name(file: pd.ExcelFile):
        sheets = file.sheet_names
        name = ""
        for sh in sheets:
            name = ""
            df = pd.read_excel(file, sheet_name=sh)
            r = df.columns.to_numpy().tolist()

            startConcat = False
            for cell in r:
                if cell == "Nome:":
                    if startConcat == False:
                        startConcat = True
                    else:
                        print("Weird error in finding name")
                        name = None
                        break
                elif startConcat == True:
                    if str(cell).find(":") != -1:
                        if len(name.strip()) > 0:
                            return name.strip()
                        name = None
                        break
                    if cell != None:
                        name += " " + str(cell)
        return name

    @staticmethod
    def get_patient_data(file: pd.ExcelFile):
            data = dict()
            for m in file.sheet_names:
                if m not in ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]:
                    continue
                df = pd.read_excel(file, sheet_name=m, index_col=0, header=2)
                df = df.filter(regex='([1-9])+-\w{3}$', axis='columns')
                data[m] = df
            return data
        