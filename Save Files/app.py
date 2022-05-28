from flask import Flask
import requests
import json
import os
import torch
import datetime
import ssl
import pandas as pd


ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

response = requests.get('https://art.artisticmilliners.com:8081/ords/art/ocr/invoice/id/', verify = False).text
response_info = json.loads(response)
data=response_info['items']
Current_Date_Formatted = datetime.datetime.today().strftime ('%m%d%Y')
current_date=str(Current_Date_Formatted)
parent_dir = f'D:/Mehmaam/Save Files/'
mode = 0o666

path1 = os.path.join(parent_dir, current_date)

print("path1========>",path1)
os.mkdir(path1, mode)
dicts=data[0]
val=next(iter(dicts.values()))
val=str(val)

current_date_folder=current_date+ "/"+ val
path = os.path.join(parent_dir, current_date_folder)
os.mkdir(path, mode)
print("path========>",path)
print("Directory '% s' created" % current_date_folder)




#'C:/Users/Naeem/Desktop/Save Files/'        
app.config['UPLOAD_FOLDER'] = path


