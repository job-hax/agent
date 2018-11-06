import requests
from .models import Profile

def get_profile(user):
    social = user.social_auth.get(provider='linkedin-oauth2')
    token = social.extra_data['access_token']
    r = requests.get('https://api.linkedin.com/v1/people/~:(id,first-name,last-name,maiden-name,formatted-name,phonetic-first-name,phonetic-last-name,formatted-phonetic-name,headline,location,industry,current-share,num-connections,num-connections-capped,summary,specialties,positions,picture-url,site-standard-profile-request,api-standard-profile-request,public-profile-url,email-address)?format=json', headers={'Authorization': 'Bearer ' + token})
    profile = Profile.objects.get(user=user)
    profile.linkedin_info = r.text
    profile.save()