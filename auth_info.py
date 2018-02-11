from requests import request, ConnectionError
from django.http import HttpResponse, Http404
from .models import Profile


def save_profile(user, response, *args, **kwargs):
  if response.get('image') and response['image'].get('url'):
    url = response['image'].get('url')
    user.profile.avatar_url = url
    user.save()
    
