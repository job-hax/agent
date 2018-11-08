from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('metrics', views.metrics, name='metrics'),
    path('job_board', views.job_board, name='job_board'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('jobdetails', views.jobdetails, name='jobdetails'),
    path('deleteJobApplication', views.deleteJobApplication, name='deleteJobApplication'),
    path('updateJobApplication', views.updateJobApplication, name='updateJobApplication'),
    path('filterJobApplications', views.filterJobApplications, name='filterJobApplications'),
    path('get_total_application_count', views.get_total_application_count, name='get_total_application_count'),
    path('get_application_count_by_month', views.get_application_count_by_month, name='get_application_count_by_month'),
    path('addJobApplication', views.addJobApplication, name='addJobApplication'),
    url('', include('social_django.urls', namespace='social')),
    path('dashboard', views.dashboard, name='dashboard')
]
