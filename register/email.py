from django.conf import settings
import mandrill

def send_email(body, subject, from_, to):
    mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
    message = {
    	'from_email': from_,
    	'from_name': 'Green Streets Initiative - W/R Day Registration',
    	'metadata': {
            'website': 'checkin-greenstreets.rhcloud.com'
        },
    	'to': [{
            'email': to,
    	    'type': 'to'
        }],
    	'subject': subject,
    	'text': body
    }
    try:
        mandrill_client.messages.send(message=message, async=True)
    except mandrill.Error:
        pass


def registration_confirmation_email(body):
    send_email(body, \
        'New Walk/Ride Registrant!',\
        'registration@gogreenstreets.org',\
        'gustavo@gogreenstreets.org')
