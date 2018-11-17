from django.test import TestCase

# Create your tests here.
from accounts.models import ApplicationStatus, JobApplication, Profile, JobPostDetail
from django.contrib.auth.models import User

class ApplicationStatusModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ApplicationStatus.objects.create(value='N/A')
        ApplicationStatus.objects.create(value='In Progress')
        ApplicationStatus.objects.create(value='Success')
        ApplicationStatus.objects.create(value='Fail')

    def test_first_status(self):
        applicationStatus = ApplicationStatus.objects.get(id=1)
        self.assertEquals(applicationStatus.value, 'N/A')  

class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create(username='user1')

    def test_change_profile(self):
        user = self.user
        profile = Profile.objects.get(user = user)
        profile.linkedin_info='{test : test}'
        profile.save()
        linkedin_info = Profile.objects.get(user=user).linkedin_info
        self.assertEquals(profile.linkedin_info, linkedin_info)   

class JobApplicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create(username='user1')
        cls.status = ApplicationStatus.objects.create(value='N/A')

    def test_create_job_application(self):
        user = self.user
        ja = JobApplication.objects.create(jobTitle='jobTitle', company='company', applyDate='2018-01-01', msgId=123123, 
        source = 'source', user = user, companyLogo = 'companyLogo', applicationStatus = self.status)
        self.assertEquals(ja, JobApplication.objects.get(id=1))             

class JobPostDetailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create(username='user1')
        cls.status = ApplicationStatus.objects.create(value='N/A')
        cls.japp = JobApplication.objects.create(jobTitle='jobTitle', company='company', applyDate='2018-01-01', msgId=123123, 
        source = 'source', user = cls.user, companyLogo = 'companyLogo', applicationStatus = cls.status)

    def test_create_job_post_detail(self):
        japp_details = JobPostDetail(job_post = self.japp, posterInformation = '{}', decoratedJobPosting = '{}', topCardV2 = '{}')
        japp_details.save()
        self.assertEquals(japp_details, JobPostDetail.objects.get(job_post=self.japp))