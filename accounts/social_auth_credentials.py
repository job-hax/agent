# github.com/python-social-auth/social-core/issues/125
from datetime import datetime

from requests import exceptions as requests_errors

from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials as GoogleCredentials

from googleapiclient import discovery

from social_django.utils import load_strategy

class Credentials(GoogleCredentials):
    """Google auth credentials using python social auth under the hood"""

    def _parse_expiry(self, data):
        """
        Parses the expiry field from a data into a datetime.

        Args:
             data (Mapping): extra_data from UserSocialAuth model
        Returns:
             datetime: The expiration
        """
        return datetime.fromtimestamp(data['auth_time'] + data['expires'])

    def __init__(self, usa):
        """
        Args:
            usa (UserSocialAuth): UserSocialAuth google-oauth2 object
        """
        backend = usa.get_backend_instance(load_strategy())
        data = usa.extra_data
        token = data['access_token']
        refresh_token = data['refresh_token']
        token_uri = backend.refresh_token_url()
        client_id, client_secret = backend.get_key_and_secret()
        scopes = backend.get_scope()
        # id_token is not provided with GoogleOAuth2 backend
        super().__init__(
            token, refresh_token=refresh_token, id_token=None,
            token_uri=token_uri, client_id=client_id, client_secret=client_secret,
            scopes=scopes
        )
        self.usa = usa
        # Needed for self.expired() check
        self.expiry = self._parse_expiry(data)

    def refresh(self, request):
        """Refreshes the access token.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Raises:
            google.auth.exceptions.RefreshError: If the credentials could
                not be refreshed.
        """
        usa = self.usa
        try:
            usa.refresh_token(load_strategy())
        except requests_errors.HTTPError as e:
            raise RefreshError(e)
        data = usa.extra_data
        self.token = data['access_token']
        self._refresh_token = data['refresh_token']
        self.expiry = self._parse_expiry(data)
