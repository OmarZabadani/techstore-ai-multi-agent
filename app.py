import zipfile

zip_path = r"D:\download\training_AI\weak 7 and 8\dataset\TechStore_AI_Agent_Training_Data.zip"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    print(zip_ref.namelist())

