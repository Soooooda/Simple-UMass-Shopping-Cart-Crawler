from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import re
import smtplib, ssl
# from apiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def sendmail(str1):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    msg = create_message("gsoooda@gmail.com", "xgong@umass.edu", "Open class test", str(str1))
    send_message(service,"gsoooda@gmail.com",msg)

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])


def create_draft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()

    print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

    return draft
  except errors.HttpError:
    # print('An error occurred: %s' % error)
    return None


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError:
    print(errors.HttpError)
    print('An error occurred')


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
#   return {'raw': base64.urlsafe_b64encode(message.as_string())}
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}




def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  # return {'raw': base64.urlsafe_b64encode(message.as_string())}
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
    login_data = {'userid':'yourSpireID','pwd':'yourPassword'}
    url = 'https://www.spire.umass.edu/psp/heproda/?cmd=login&languageCd=ENG'

    session = requests.Session()
    session.post(url,headers = headers,data = login_data)

    set_interface_data = {'ICAction': 'UM_DERIVED_CC_UM_MOBILE_VIEW','ICSID': '32YQemQoBj0bGANob7sIad82N92NYMMJ5lHH/w6yXTU='}
    url2 = 'https://www.spire.umass.edu/psc/heproda/EMPLOYEE/SA/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=GRAD&EMPLID=32286346&INSTITUTION=UMAMH&STRM=1207'
    response = session.get(url2,headers = headers)
    print("succeed! ",response.status_code)

    if response.status_code!=200:
        sendmail(response.status_code)
        flag = False
        
    # print(response.text)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())

    mytrs = soup.findAll("tr", {"valign":"center"})


    for e in mytrs:
        # print(e.prettify())
        print(e.a.getText())
        for x in e.find('img')['src'].split('_'):
            if x=="OPEN" or x=="WAITLIST":
                print(x)
                sendmail(e.a.getText())
            elif x=="CLOSED":
                print(x)
                # sendmail(e.a.getText())
            elif x=="ENROLLED":
                print(x)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
