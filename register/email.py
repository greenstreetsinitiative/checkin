from django.conf import settings
import mandrill

def send_email_from_form(form):
    mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
    body = 'Hello'
    message = {
    	'from_email': 'registration@gogreenstreets.org',
    	'from_name': 'Green Streets Initiative - W/R Day Registration',
    	'metadata': {
            'website': 'checkin-greenstreets.rhcloud.com'
        },
    	'to': [{
            'email': 'gustavo@gogreenstreets.org',
    	    'type': 'to'
        }],
    	'subject': 'New Walk/Ride Registrant!',
    	'text': body
    }
    try:
        mandrill_client.messages.send(message=message, async=True)
    except mandrill.Error:
        pass
