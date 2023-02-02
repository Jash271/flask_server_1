from __future__ import print_function
from flask import Flask,render_template
from flask import request
from werkzeug.utils import secure_filename
import os
"""
Gmail API

"""
#########################


import os.path
import base64
import email
import html.parser
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
######################
app = Flask(__name__)
upload_folder = 'tokens'
app.config['UPLOAD_FOLDER'] = upload_folder
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

@app.route("/")
def hello_world():
    # return  render index.html file
    return render_template("index.html")
    

@app.route("/accept_file",methods = ['POST','GET'])
def accept_file():
    print(request.files)
    file = request.files['file']
    #Save File
    filename = 'Jash'+ "."+ file.filename.split(".")[-1]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return {
        "ok":1
    }

@app.route("/login",methods = ['POST','GET'])
def get_email_data():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES,)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        """
        get_email_data(service,'186064f58a574920')
        print('################################################################################################')
        get_email_data(service,'185fc4fa5d982eda')
        print('################################################################################################')
        get_email_data(service,'185f29195ee26c4b')
        """
        #return
        results = service.users().labels().list(userId='me').execute()
        print(results)

        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        print(labels)
        # for label in labels:
            # print(type(label))
            # print(label['name'])
        return {
            "ok":1,
        }

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        return {
            "ok":0,
            "error":error
        }

@app.route("/sample",methods = ['POST','GET'])
def sample():
    return render_template("sample.html")
if __name__ == "_main_":
  app.run()