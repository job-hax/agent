### Quickstart

1. Install Postgres database depending on your [OS](https://www.postgresql.org/download/):
```
brew install postgres
```

2. Run install script:
```
./src/install.sh
```

3. In [Google Google Developers](https://console.developers.google.com/apis/library?project=_) Console  create a project:

a) Create OAuth client ID for Web Application under Credentials menu.

b) Enter the following URI's in Authorized redirect URIs list: 
```
http://localhost:8000/accounts/complete/google-oauth2/
http://127.0.0.1:8000/accounts/complete/google-oauth2/
```
c) Under the APIs and services tab, search for Google+ API and Gmail API and enable them.

4. Set SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET environment variables:
```
export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=''  #Paste CLient Key
export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET= '' #Paste Secret Key
```

5. In [LinkedIn Developer Network](https://www.linkedin.com/secure/developer) create a project ([Instructions in STEP 1](https://developer.linkedin.com/docs/oauth2#)):

a) Enter the following URI in Authorized redirect URIs list: 
```
http://127.0.0.1:8000/accounts/complete/linkedin-oauth2/
```

6. Set SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY and SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET environment variables:
```
export SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY=''  #Paste CLient Key
export SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET= '' #Paste Secret Key
```

7. Start server:
```
./src/start.sh
```

