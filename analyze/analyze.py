import pandas as pd
import os

ROOT_DIR = os.path.abspath(os.curdir)
DEFAULT_ORIG_FOLDER_PATH = os.path.join(ROOT_DIR, "original")
class Analyze:
    original_folder_path: str
    patients_files: list[os.DirEntry]
    
    def __init__(self, original_folder_path: str) -> None:
        if not os.path.exists(original_folder_path):
            print(
                "[WARNING] Original files folder was not found, one will be created for you in ./original."
            )
            os.makedirs(DEFAULT_ORIG_FOLDER_PATH, exist_ok=True)

        original_dir = Analyze.get_dir(original_folder_path)
        valid_files = list(filter(Analyze.is_file_valid, original_dir))

        print(valid_files)

        self.original_folder_path = original_folder_path
        self.patients_files = valid_files

    @staticmethod
    def get_dir(path: str):
        return list(os.scandir(path))
    
    @staticmethod
    def is_file_valid(file: os.DirEntry):
        if str(file.name).find(".xlxs") == -1 and str(file.name).find(".xls") == -1:
            return False
        return True