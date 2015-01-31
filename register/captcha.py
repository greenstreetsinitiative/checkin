from django.conf import settings
import requests

# Credit: http://stackoverflow.com/a/5976065
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def captcha_invalid(request):
    """
    Verifies captcha
    https://developers.google.com/recaptcha/
    """
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': settings.SECRET_RECAPTCHA_KEY,
        'response': request.POST['g-recaptcha-response'],
        'remoteip': get_client_ip(request)
    }
    r = requests.get(url, params=payload)
    return r.json()['success']
