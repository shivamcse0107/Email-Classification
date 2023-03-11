import os
import requests
import pathlib
import csv
from read_params import read_params

config = read_params('config.yaml')
def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def CheckFiles(subject_name):
    responses = []
    folder_path = config['base']['directoryPath']
    directoryPath = os.path.join(folder_path, "{}".format(clean(subject_name)))
    if os.listdir(directoryPath)== []:
        return False
    else:
        pdf_paths = [x for x in pathlib.Path(directoryPath).rglob('*.pdf')]
        jpg_paths = [x for x in pathlib.Path(directoryPath).rglob('*.jpg')]
        png_paths = [x for x in pathlib.Path(directoryPath).rglob('*.png')]
        paths = pdf_paths+jpg_paths+png_paths
        for path in paths:
            files = {"file_path":open(str(path),'rb')}
            response = requests.post("http://127.0.0.1:3009/files_v1.0",files = files)
            print(response.json())
            if response.json()['status']==200:
                resp = response.json()['extraction_result']

                csv_path = "processed_pdf/{}.csv".format(clean(subject_name))
                with open(csv_path, 'w') as csv_file:  
                    writer = csv.writer(csv_file)
                    for key, value in resp.items():
                        writer.writerow([key, value])
            else:
                resp = response.json()['error']
                csv_path = "processed_pdf/{}.csv".format(clean(subject_name))
                with open(csv_path, 'w') as csv_file:  
                    writer = csv.writer(csv_file)
                    for key, value in resp.items():
                        writer.writerow([key, value])

 