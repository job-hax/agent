from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient import errors
from .models import Profile
import string
from datetime import datetime
import requests

from requests import exceptions as requests_errors

from google.auth.exceptions import RefreshError
from .social_auth_credentials import Credentials
from social_django.utils import load_strategy

from .models import JobApplication
from .models import ApplicationStatus
from .models import JobPostDetail
import base64
import time
from .gmail_utils import convertTime
from .gmail_utils import removeHtmlTags
from .gmail_utils import find_nth
from .linkedin_utils import parse_job_detail

def get_email_detail(service, user_id, msg_id, user, source):
  """Get a Message with given ID.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.
  Returns:
    A Message.
  """
  try:
    custom_image_url = '/static/img/errorcvlogotemporary.png'
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    jobTitle = ''
    company = ''
    image_url = ''
    for header in message['payload']['headers']:
        if header['name'] == 'Subject':
            subject = str(header['value'])
            if(source == 'LinkedIn'):
                jobTitle = subject[subject.index('for ') + 4 : subject.index(' at ')]
                company = subject[subject.index('at ') + 3:]
            elif(source == 'Hired.com'):
                jobTitle = subject[subject.index('st: ') + 4 : subject.index(' at ')]
                company = subject[subject.index('at ') + 3 : subject.index('(')]
            elif(source == 'Indeed'):
                jobTitle = subject[subject.index('Indeed Application: ') + 20 : ]
        elif header['name'] == 'Date':
            date = header['value']
            date = convertTime(str(date))
    try:
        for part in message['payload']['parts']:
            if(part['mimeType'] == 'text/html'):
                #get mail's body as a string
                body = str(base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')))
                if(source == 'LinkedIn'):
                    posterInformationJSON, decoratedJobPostingJSON, topCardV2JSON = parse_job_detail(body)
                    s = find_nth(body, 'https://media.licdn.com', 2)
                    if(s != -1):
                        e = find_nth(body, '" alt="' + company + '"', 1)
                        image_url = body[s : e].replace('&amp;', '&')
                        image_exists=requests.get(image_url)
                        if(image_exists.status_code == 404):
                            image_url = custom_image_url 
                    else:
                        image_url = custom_image_url
                    if len(image_url) > 300:
                        image_url = custom_image_url
                elif(source == 'Vettery'):
                    jobTitle = body[body.index('Role: ') + 6 : body.index('Salary')]
                    jobTitle = removeHtmlTags(jobTitle)
                    company = body[body.index('interview with ') + 15 : body.index('. Interested?')]
                    image_url = custom_image_url
                elif(source == 'Indeed'):
                    company = body[body.index('Get job updates from <b>') + 24 : body.index('</b>.<br><i>By selecting')]
                    image_url = custom_image_url
                elif(source == 'Hired.com'):
                    image_url = custom_image_url    
    except Exception as e:
        print(e)

    if user.is_authenticated:
      inserted_before = JobApplication.objects.all().filter(msgId=msg_id)
      print(image_url)
      if not inserted_before and jobTitle != '' and company != '':
        status = ApplicationStatus.objects.all().get(value='N/A')
        japp = JobApplication(jobTitle=jobTitle, company=company, applyDate=date, msgId=msg_id, source = source, user = user, companyLogo = image_url, applicationStatus = status)
        japp.save()
        if(source == 'LinkedIn'):
            japp_details = JobPostDetail(job_post = japp, posterInformation = posterInformationJSON, decoratedJobPosting = decoratedJobPostingJSON, topCardV2 = topCardV2JSON)
            japp_details.save()
  except errors.HttpError as error:
    print('An error occurred: %s' % error)



def get_emails_with_custom_query(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query, includeSpamTrash=True).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token, includeSpamTrash=True).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def fetchJobApplications(user):
    time_string = ''
    #checks user last update time and add it as a query parameter
    profile = Profile.objects.get(user=user)
    if profile.gmail_last_update_time != 0:
        time_string = ' AND after:' + str(profile.gmail_last_update_time)
        print('its not the first time query will be added : ' + time_string)
    else:
        print('its the first time.. so we are querying all mails')

    #initiates Gmail API
    usa = user.social_auth.get(provider='google-oauth2')
    GMAIL = build('gmail', 'v1', credentials=Credentials(usa))

    #retrieves user email's with custom query parameter
    linkedInMessages = get_emails_with_custom_query(GMAIL, 'me', 'from:jobs-listings@linkedin.com AND subject:You applied for' + time_string)# AND after:2018/01/01')
    hiredMessages = get_emails_with_custom_query(GMAIL, 'me', 'from:reply@hired.com AND subject:Interview Request' + time_string)
    #vetteryMessages = get_emails_with_custom_query(GMAIL, 'me', 'from:@connect.vettery.com AND subject:Interview Request' + time_string)
    indeedMessages = get_emails_with_custom_query(GMAIL, 'me', 'from:indeedapply@indeed.com AND subject:Indeed Application' + time_string)

    #retvieves specific email's detail one by one
    for message in linkedInMessages:
        get_email_detail(GMAIL, 'me', message['id'], user, 'LinkedIn')
    for message in hiredMessages:
        get_email_detail(GMAIL, 'me', message['id'], user, 'Hired.com')
    for message in indeedMessages:
        get_email_detail(GMAIL, 'me', message['id'], user, 'Indeed')
    #for message in vetteryMessages:
    #    GetMessage(GMAIL, 'me', message['id'], user, 'Vettery')

    #updates user last update time after all this
    now = datetime.utcnow().timestamp()
    profile.gmail_last_update_time = now
    profile.save()
