import json

import requests
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver


@receiver(user_logged_in)
def add_phone_to_extra_data(request, user, **kwargs):
    phone = None
    social = SocialAccount.objects.get(user=user)
    token = kwargs['sociallogin'].token.token
    response = requests.get(
        'https://people.googleapis.com/v1/people/me?personFields=phoneNumbers',
        params={'access_token': token}
    )

    data = json.loads(response.text)

    if 'phoneNumbers' in data and data['phoneNumbers']:
        phone = data['phoneNumbers'][0]['canonicalForm']
    social.extra_data['phone'] = phone
    social.save()
