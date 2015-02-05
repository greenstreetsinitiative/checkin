from django.conf import settings
import requests

def get_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR')

def captcha_invalid(request):
    """ https://developers.google.com/recaptcha/ """
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': settings.SECRET_RECAPTCHA_KEY,
        'response': request.POST['g-recaptcha-response'],
        'remoteip': get_ip(request)
    }
    r = requests.get(url, params=payload)
    return r.json()['success']
