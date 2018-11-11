from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import JobApplication
from .models import ApplicationStatus
from .models import Profile
from .models import JobPostDetail
from .gmail_lookup import fetchJobApplications
from .linkedin_lookup import get_profile
from django.http import HttpResponseRedirect
from background_task import background
from django.db.models import Q
import datetime
from dateutil import tz
from django.db.models import Count
from django.core import serializers
import json
from django.http import JsonResponse

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')

def update_user(request):
  user = request.user
  user.username = request.POST['newusername']    
  user.first_name = request.POST['newuserfirstname']    
  user.last_name = request.POST['newuserlastname']  
  user.save()  
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_account(request):
  request.user.delete()
  auth.logout(request)
  return redirect('index')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

def updateJobApplication(request):
  if request.method == 'POST':
    user_job_app = JobApplication.objects.get(pk=request.POST['pk'])
    status = request.POST['ddStatus']
    user_job_app.applicationStatus = ApplicationStatus.objects.get(pk=status)
    user_job_app.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    return dashboard(request)

def deleteJobApplication(request):
  if request.method == 'POST':
    user_job_app = JobApplication.objects.get(pk=request.POST['pk'])
    user_job_app.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    return dashboard(request)    

@background(schedule=1)
def scheduleFetcher(user_id):
    user = User.objects.get(pk=user_id)
    if user.social_auth.filter(provider='google-oauth2'):
        fetchJobApplications(user)

def getStatuses(request):
  statuses = ApplicationStatus.objects.all()
  data = serializers.serialize("json", statuses)  
  return JsonResponse(data)

def dashboard(request):
  user_job_apps = JobApplication.objects.filter(user_id=request.user.id).order_by('-applyDate')
  statuses = ApplicationStatus.objects.all()

  if len(statuses) == 0:
    dummyStatus = ApplicationStatus(value = 'N/A')
    dummyStatus.save()
    dummyStatus = ApplicationStatus(value = 'Planning')
    dummyStatus.save()
    dummyStatus = ApplicationStatus(value = 'In Progress')
    dummyStatus.save()
    dummyStatus = ApplicationStatus(value = 'Offer')
    dummyStatus.save()
    dummyStatus = ApplicationStatus(value = 'Fail')
    dummyStatus.save()
    statuses = ApplicationStatus.objects.all()

  #it'll be used for background tasking in production
  #refs. https://medium.com/@robinttt333/running-background-tasks-in-django-f4c1d3f6f06e
  #https://django-background-tasks.readthedocs.io/en/latest/
  #https://stackoverflow.com/questions/41205607/how-to-activate-the-process-queue-in-django-background-tasks
  #scheduleFetcher.now(request.user.id)
  scheduleFetcher(request.user.id)

  if request.user.social_auth.filter(provider='linkedin-oauth2'):
        get_profile(request.user)

  profile = Profile.objects.get(user_id= request.user.id)
  if(profile.gmail_last_update_time == 0):
    last_sync_time = "Syncing..."
  else:
    last_sync_time = datetime.datetime.utcfromtimestamp(profile.gmail_last_update_time)
  context = {
    'job_apps': user_job_apps,
    'last_sync_time': last_sync_time,
    'statuses': statuses
  }
  return render(request, 'accounts/dashboard.html', context)

def addJobApplication(request):
 if request.method == 'POST':
   body = json.loads(request.body)
   job_title = body['job_title']
   company = body['company']
   applicationdate = body['applicationdate']
   status = int(body['status'])
   source = body['source']
  
   japp = JobApplication(jobTitle=job_title, company=company, applyDate=applicationdate, msgId='', source =source, user = request.user, companyLogo = '/static/img/errorcvlogotemporary.png')
   japp.applicationStatus = ApplicationStatus.objects.get(pk=status)
   japp.save()
   
   return JsonResponse({'success':True})

def filterJobApplications(request):
  if request.method == 'POST':
    start = request.POST['start']
    end = request.POST['end']
    query = JobApplication.objects.filter(user_id=request.user.id)
    if start != '':
      query = query.filter(applyDate__gte=start)
    if end != '':
      query = query.filter(applyDate__lte=end)
    user_job_apps = query.order_by('-applyDate')
    statuses = ApplicationStatus.objects.all()
    profile = Profile.objects.get(user_id = request.user.id)
    if(profile.gmail_last_update_time == 0):
      last_sync_time = "Syncing..."
    else:
      last_sync_time = datetime.datetime.fromtimestamp(profile.gmail_last_update_time)
    context = {
      'job_apps': user_job_apps,
      'last_sync_time': last_sync_time,
      'statuses': statuses
    }
    return render(request, 'accounts/dashboard.html', context)
  else:
    return dashboard(request)

def metrics(request):
  context = {

  }
  return render(request, 'accounts/metrics.html', context)

def job_board(request):
  context = {

  }
  return render(request, 'accounts/job_board.html', context)

def profile(request):
  context = {

  }
  return render(request, 'accounts/profile.html', context)

def settings(request):
  context = {

  }
  return render(request, 'accounts/settings.html', context)

def jobdetails(request):
  context = {

  }
  return render(request, 'accounts/jobdetails.html', context)

def wordcloud(request):
  context = {

  }
  return render(request, 'accounts/metrics/wordcloud.html', context)

def get_job_detail(request): 
  id = request.GET['pk'] 
  app = JobApplication.objects.all().get(pk = id)
  try:
    details = JobPostDetail.objects.all().get(job_post = app)
    context = {
        'posterInformation': json.dumps(details.posterInformation),
        'decoratedJobPosting': json.dumps(details.decoratedJobPosting),
        'topCardV2': json.dumps(details.topCardV2),
        'job': app
    }
  except:
    context = {
        'posterInformation': '{}',
        'decoratedJobPosting': '{}',
        'topCardV2': '{}',
        'job': app
    }
  print(context)
  return render(request, 'accounts/jobdetails.html', context)

def get_total_application_count(request):
  count = JobApplication.objects.filter(user_id=request.user.id).count()
  return JsonResponse({'count':count})

def get_application_count_by_month(request):
  response = []
  sources = ['Hired.com','LinkedIn','Indeed', 'Others']
  for i in sources:
    if i != 'Others':
      appsByMonths = JobApplication.objects.filter(user_id=request.user.id,source=i,applyDate__year='2018').values('applyDate__year', 'applyDate__month').annotate(count=Count('pk'))
    else:  
      appsByMonths = JobApplication.objects.filter(~Q(source = 'LinkedIn'),~Q(source = 'Hired.com'),~Q(source = 'Indeed'),user_id=request.user.id,applyDate__year='2018').values('applyDate__year', 'applyDate__month').annotate(count=Count('pk'))
    item = {}
    item['source'] = i
    data = [0] * 12
    for app in appsByMonths:
      data[app['applyDate__month'] - 1] = app['count']
    item['data'] = data  
    response.append(item)
  return JsonResponse(response, safe=False)

def get_application_count_by_month_with_total(request):
  response = []
  sources = ['Hired.com','LinkedIn','Indeed', 'Others', 'Total']
  for i in sources:
    if i == 'Total':
      appsByMonths = JobApplication.objects.filter(user_id=request.user.id,applyDate__year='2018').values('applyDate__year', 'applyDate__month').annotate(count=Count('pk'))
    elif i != 'Others':
      appsByMonths = JobApplication.objects.filter(user_id=request.user.id,source=i,applyDate__year='2018').values('applyDate__year', 'applyDate__month').annotate(count=Count('pk'))
    else:  
      appsByMonths = JobApplication.objects.filter(~Q(source = 'LinkedIn'),~Q(source = 'Hired.com'),~Q(source = 'Indeed'),user_id=request.user.id,applyDate__year='2018').values('applyDate__year', 'applyDate__month').annotate(count=Count('pk'))
    item = {}
    item['source'] = i
    data = [0] * 12
    for app in appsByMonths:
      data[app['applyDate__month'] - 1] = app['count']
    item['data'] = data  
    response.append(item)
  return JsonResponse(response, safe=False)  

def get_count_by_statuses(request):
  statuses = JobApplication.objects.filter(~Q(applicationStatus = None),user_id=request.user.id).values('applicationStatus').annotate(count=Count('pk'))
  response = []
  for i in statuses:
    item = {}
    item['name'] = ApplicationStatus.objects.get(pk=i['applicationStatus']).value
    item['value'] = i['count']
    response.append(item)
  return JsonResponse(response, safe=False)
  

def get_count_by_jobtitle_and_statuses(request):
  response = {}
  job_titles = JobApplication.objects.filter(~Q(applicationStatus = None),user_id=request.user.id).values('jobTitle').annotate(count=Count('pk'))
  jobs = []
  statuses_data = []
  status_data = []
  for job_title in job_titles:
    jobs.append(job_title['jobTitle'])
  response['jobs'] = jobs
  statuses = ApplicationStatus.objects.all()
  for status in statuses:
    statuses_data.append(status.value)
    item = {}
    item['name'] = status.value
    data = [0] * len(job_titles)
    for i,job_title in enumerate(job_titles):
      data[i] = JobApplication.objects.filter(user_id=request.user.id, jobTitle=job_title['jobTitle'], applicationStatus=status).count()
    item['data'] = data
    status_data.append(item)
  response['statuses'] = statuses_data  
  response['data'] = status_data  
  return JsonResponse(response, safe=False)