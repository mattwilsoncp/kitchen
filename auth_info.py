from requests import request, ConnectionError
from django.http import HttpResponse, Http404
from .models import Profile
from django.shortcuts import redirect


def save_profile(user, response, *args, **kwargs):
  if response.get('image') and response['image'].get('url'):
    url = response['image'].get('url')
    user.profile.avatar_url = url
    user.save()

def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
    if backend.name == 'google-oauth2' and social and \
       response.get('refresh_token') is None and \
       social.extra_data.get('refresh_token') is None:
        return redirect('/login/google-oauth2?approval_prompt=force')
