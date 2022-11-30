from __future__ import print_function
import pickle
import os.path
import io
import shutil
from typing import ItemsView
import requests
from Aesdecrypt import *
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from docx import Document 
class DriveAPI:
		global SCOPES
		
		# Define the scopes
		SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']

		def __init__(self):
			
			# Variable self.creds will
			# store the user access token.
			# If no valid token found
			# we will create one.
			self.creds = None

			# The file token.pickle stores the
			# user's access and refresh tokens. It is
			# created automatically when the authorization
			# flow completes for the first time.

			# Check if file token.pickle exists
			if os.path.exists('token.pickle'):

				# Read the token from the file and
				# store it in the variable self.creds
				with open('token.pickle', 'rb') as token:
					self.creds = pickle.load(token)

			# If no valid credentials are available,
			# request the user to log in.
			if not self.creds or not self.creds.valid:

				# If token is expired, it will be refreshed,
				# else, we will request a new one.
				if self.creds and self.creds.expired and self.creds.refresh_token:
					self.creds.refresh(Request())
				else:
					flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
					self.creds = flow.run_local_server(port=0)

				# Save the access token in token.pickle
				# file for future usage
				with open('token.pickle', 'wb') as token:
					pickle.dump(self.creds, token)

			# Connect to the API service
			self.service = build('drive', 'v3', credentials=self.creds)

			# request a list of first N files or
			# folders with name and id from the API.
			results = self.service.files().list(
				pageSize=100, fields="files(id, name)").execute()
			items = results.get('files', [])

		def FileDownload(self, file_id, file_name):
			request = self.service.files().get_media(fileId=file_id)
			fh = io.BytesIO()
			
			# Initialise a downloader object to download the file
			downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
			done = False

			try:
				# Download the data in chunks
				while not done:
					status, done = downloader.next_chunk()

				fh.seek(0)
				finalpath=''
				pathname="E:\College\Capstone Project\Something new\Downloads"
				pathname=pathname+'\\'
				finalpath=pathname+file_name
				# Write the received data to the file
				with open(finalpath, 'wb') as f:
					shutil.copyfileobj(fh, f)
				#print("File Downloaded")
				# Return True if file Downloaded successfully
				return True
				
			except:
				
				# Return False if something went wrong
				#print("Something went wrong.")

				return False

def down(name,id):
	obj = DriveAPI()
	f_id = id
	f_name = name
	obj.FileDownload(f_id, f_name)

def newfiledox(data,file_name):
	downloadpath=''
	dataf=''
	path="E:\College\Capstone Project\Something new\decrypted_files"
	path=path+'\\'
	downloadpath=path+file_name
	downloadpath=downloadpath[:-3]
	downloadpath=downloadpath+'docx'
	doc = Document()
	temp=data.splitlines()
	for i in temp:
		dataf=dataf+i+'\n'
	doc.add_paragraph(dataf)
	doc.save(downloadpath)

def newfile(data,file_name):
	downloadpath=''
	path="E:\College\Capstone Project\Something new\decrypted_files"
	path=path+'\\'
	downloadpath=path+file_name
	temp=data.splitlines()
	print(temp)
	open(downloadpath, 'w').close()
	with open(downloadpath, 'w') as k:
		k.writelines("%s\n" % l for l in temp)

