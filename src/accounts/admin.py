from django.contrib import admin
from .models import JobApplication, ApplicationStatus, Profile, JobPostDetail

# Register your models here.
admin.site.register(JobApplication)
admin.site.register(ApplicationStatus)
admin.site.register(Profile)
admin.site.register(JobPostDetail)
