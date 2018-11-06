from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail_last_update_time = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class ApplicationStatus(models.Model):
  value = models.CharField(max_length=20)
  def __str__(self):
    return self.value  

class JobApplication(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
  applicationStatus = models.ForeignKey(ApplicationStatus, on_delete=models.DO_NOTHING, null=True, blank=True)
  jobTitle = models.CharField(max_length=200)
  company = models.CharField(max_length=200)
  companyLogo = models.CharField(max_length=200, null=True, blank=True)
  applyDate = models.CharField(max_length=200)
  msgId = models.CharField(max_length=200)
  source = models.CharField(max_length=200, default='')
  def __str__(self):
    return self.jobTitle + '@' + self.company

class JobPostDetail(models.Model):
  job_post = models.ForeignKey(JobApplication, on_delete=models.DO_NOTHING, null=True, blank=True) 
  posterInformation = models.TextField(null=True, blank=True)
  decoratedJobPosting = models.TextField(null=True, blank=True)
  topCardV2 = models.TextField(null=True, blank=True)
