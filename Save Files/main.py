import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
#import magic
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import cv2
import ssl
import sys
from PIL import Image 
import PIL 
from pylab import rcParams
from IPython.display import Image
import easyocr
import re
import json
import camelot
import pytesseract
import requests
from pdf2image import convert_from_path
ssl._create_default_https_context = ssl._create_unverified_context





ALLOWED_EXTENSIONS = set(['pdf'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			f1=os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(f1)
			print("F1=======>",f1)
			print("filename=======>",filename)
			print("File=======>",file)
			print("App config=======>",app.config['UPLOAD_FOLDER'])
		#	print("file name",filename)
			flash('File successfully uploaded')
			rcParams['figure.figsize'] = 8, 16
			reader = easyocr.Reader(['en'])			
			'''
			Part #1 : Converting PDF to images
			'''
			
			# Store all the pages of the PDF in a variable
			pages = convert_from_path(f1, 500,poppler_path=r'C:\\Users\\Administrator\\Downloads\\poppler-0.68.0\\bin')
			
			# Counter to store images of each page of PDF to image
			image_counter = 1
			
			# Iterate through all the pages stored above
			for page in pages:
			
				filename = "page_"+str(image_counter)+".jpg"
				
				# Save the image of the page in system
				page.save(filename, 'JPEG',dpi=(300,300))
				#im.save("test-600.png", dpi=(600,600))
				# Increment the counter to update filename
				image_counter = image_counter + 1

			'''
			Part #2 - Recognizing text from the images using OCR
			'''
				
			# Variable to get count of total number of pages
			filelimit = image_counter-1
			
			# Creating a text file to write the output
			outfile = "out_text.txt"
			
			# Open the file in append mode so that 
			# All contents of all images are added to the same file
			f = open(outfile, "a")
			
			# Iterate from 1 to total number of pages
			for i in range(1, filelimit + 1):
			
				filename = "page_"+str(i)+".jpg"
				
			
				text = reader.readtext(filename)
				
				
				
				
				# print(text)
				# print("===============Type=====================",type(text))
				length=len(text)
				# print("====================Length===============",length)
				
					
				texts=str(text)
				# Finally, write the processed text to the file.
				f.write(texts)
			
			# Close the file after writing all the text.
			f.close()
			lst=[]
			for i in range(length):
				lst.append(text[i][1])

			str1 = ' '.join(lst)
		
			NTN_pattern="\d{7}-\w{2}"
			NTN=re.findall(NTN_pattern,str1)
			#PO correct
			po_pattern="PO#\d{5,6},|PO#\d{5,6}$| PO#\d{5,6} "
			po=re.findall(po_pattern,str1)
			#Invoice
			IN_pattern="INVOICE NO: \d{6}"
			IN=re.findall(IN_pattern,str1)

			new_po = []

			for string in po:
				new = string.replace("PO#", "")
				news = new.replace(",", "")
				new_po.append(news)







			#Order
			Order_pattern="\d{8}"
			OR=re.findall(Order_pattern,str1)
			ntn=NTN[0]
			ora=OR[0]
			data_set = {#"Party_PO": [output[36][1]],
						"National_Tax_No.": ntn,
						'Invoice No':IN,
						'Ordered No':ora,
						"PO# ":new_po,
					# "Table ": data

					}
			print(data_set)
			
			tables=camelot.read_pdf(f1 , flavor='stream', pages='1', table_areas=['5,530,620,180'])
			tables[0].parsing_report
			df=tables[0].df
			df[5]=df[5].replace(["\n"]," ",regex=True)
			df2 = df.iloc[0] #grab the first row for the header
			df = df[1:] #take the data less the header row
			df.columns = df2 #set the header row as the df header
			df.drop(columns=['PART NUMBER/DESCRIPTION'],inplace=True)
			df['LINE'].astype(bool)  
			df=df[df['LINE'].astype(bool)]
			df[['TAX RATE','EXTENDED PRICE']] = df['EXTENDED PRICE TAX RATE'].str.split(' ', 1, expand=True)
			df.drop(columns=['EXTENDED PRICE TAX RATE'],inplace=True)
			df["PO# Number"]=new_po
			df['EXTENDED PRICE'] = df['EXTENDED PRICE'].str.replace(',', '')
			df['TOTAL AMOUNT'] = df['TOTAL AMOUNT'].str.replace(',', '')
			df['QTY SHIPPED'] = df['QTY SHIPPED'].str.replace(',', '')
			df['TAX AMOUNT'] = df['TAX AMOUNT'].str.replace(',', '')			
			print(df)
			# payload={"Details": data_set,
			# "Tables":df }
			# print(payload)
			# r=requests.post("https://httpbin.org/post",data=payload)
			# print(r.text)
			return redirect('/')
		else:
			flash('Allowed file types is pdf')
			return redirect(request.url)


	

#PDF_file = "AMI Page 500.pdf"
  





if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)