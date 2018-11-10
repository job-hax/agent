from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('update_user', views.update_user, name='update_user'),
    path('metrics', views.metrics, name='metrics'),
    path('job_board', views.job_board, name='job_board'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('jobdetails', views.jobdetails, name='jobdetails'),
    path('deleteJobApplication', views.deleteJobApplication, name='deleteJobApplication'),
    path('updateJobApplication', views.updateJobApplication, name='updateJobApplication'),
    path('addJobApplication', views.addJobApplication, name='addJobApplication'),
    path('filterJobApplications', views.filterJobApplications, name='filterJobApplications'),
    path('get_total_application_count', views.get_total_application_count, name='get_total_application_count'),
    path('get_application_count_by_month', views.get_application_count_by_month, name='get_application_count_by_month'),
    path('get_application_count_by_month_with_total', views.get_application_count_by_month_with_total, name='get_application_count_by_month_with_total'),
    path('get_count_by_statuses', views.get_count_by_statuses, name='get_count_by_statuses'),
    path('get_count_by_statuses', views.get_count_by_statuses, name='get_count_by_statuses'),
    path('get_count_by_jobtitle_and_statuses', views.get_count_by_jobtitle_and_statuses, name='get_count_by_jobtitle_and_statuses'),
    path('get_job_detail', views.get_job_detail, name='get_job_detail'),
    url('', include('social_django.urls', namespace='social')),
    path('dashboard', views.dashboard, name='dashboard')
]
