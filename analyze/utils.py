import os
import pandas as pd


class Utils:
    ROOT_DIR = os.path.abspath(os.curdir)
    ORIGINAL_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/original/")
    PARAMETERS_PATH = os.path.join(ROOT_DIR, "analyze/tests/ranges.xlsx")
    TEST_OUT_FOLDER_PATH = os.path.join(ROOT_DIR, "analyze/tests/out/")

    MONTHS = [
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

    @staticmethod
    def get_dir(path: str):
        return list(os.scandir(path))

    @staticmethod
    def to_excel(file: os.DirEntry):
        return pd.ExcelFile(file)

    @staticmethod
    def rename_df_index(label: str):
        label = str(label).replace("'", "").strip()
        return label

    @staticmethod
    def rename_df_columns(label: str):
        label = str(label).strip().split("-")[0]
        return label

    @staticmethod
    def to_dict(excel: pd.ExcelFile, sheet_name: str | int):
        df = Utils.read_excel(excel, sheet_name=sheet_name)
        df = Utils.filter_df(df, "([1-9])+-\w{3}$", "columns")
        df.rename(mapper=Utils.rename_df_index, axis="index", inplace=True)

        df.fillna(-1, inplace=True)

        dup = df.columns.duplicated()
        print(df.columns)
        month = df.columns[0].split("-")[1]
        for i, col in enumerate(df.columns):
            if col.split("-")[1] != month:
                dup[i] = True
        duplicate_cols = df.columns[dup]
        df.drop(columns=duplicate_cols, inplace=True)
        df.rename(mapper=Utils.rename_df_columns, axis="columns", inplace=True)
        df.drop_duplicates(inplace=True)
        return df.to_dict()

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
            if m not in [
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
            ]:
                continue

            df = Utils.read_excel(file, m)
            df = Utils.filter_df(df, "([1-9])+-\w{3}$", "columns")
            df.drop_duplicates(inplace=True)
            reads_dict = df.to_dict()

            data[m] = reads_dict
        return data

    @staticmethod
    def read_excel(file, sheet_name) -> pd.DataFrame:
        return pd.read_excel(
            file, sheet_name=sheet_name, index_col=0, header=2, nrows=20
        )

    @staticmethod
    def filter_df(df: pd.DataFrame, pattern, axis) -> pd.DataFrame:
        return df.filter(regex=pattern, axis=axis)

    @staticmethod
    def missing_months(months):
        return [month for month in Utils.MONTHS if month not in months]

    @staticmethod
    def patient_reads(patient_excel: pd.ExcelFile, months):
        reads = {}
        for sheet_name in months:
            reads[sheet_name] = Utils.to_dict(patient_excel, sheet_name)
        return reads
