import json

from register.models import Questions, Business, Contact
from survey.models import Employer, EmplSector, EmplSizeCategory

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.core.validators import URLValidator, validate_email

def size_category_id(size):
    if size > 2000:
        return 4
    elif size > 300:
        return 3
    elif size > 51:
        return 2
    else:
        return 1

def delete_objects(*obj):
    for o in obj:
        o.delete()

class Form(object):
    """
    Django does have built in support for forms,
    """

    def __init__(self, post):
        self.post = post

        self.save_questions(post)
        self.save_business(post)

    def save_questions(self, post):
        """
        Extracts extra question inputs from the form's post request
        data and converts it to a Question model/object

        Doesn't perform any validation as the questions are all just plain
        text. At most, it checks that all the important questions are there.
        """
        q = Questions()
        try:
            q.heard_about = post['wr_hear']
            q.goals = post['wr_goals']
            if 'wr_sponsor' in post:
                q.sponsor = post['wr_sponsor']
        except KeyError:
            print 'Missing questions from form'
            raise ValidationError(_('Missing questions'), code='missing')
        q.save()
        self.questions = q

    def save_business(self, post):
        """
        Extracts information about the business/organization from the form,
        validates it and saves it to the database

        Business address isn't validated because
        """
        b = Business()
        try:
            # Get Employer model data from form
            # Sector must be handled manually right now
            e = Employer()
            e.name = post['business_name']
            e.nr_employees = int(post['business_size'])
            e.active = True
            size_cat = size_category_id(e.nr_employees)
            e.size_cat = EmplSizeCategory.objects.get(id=size_cat)
            if 'has_subteams' in post:
                e.is_parent = post['has_subteams']

            # Get Business model data from form
            if 'business_website' in post:
                b.website = post['business_website']
                URLValidator(b.website)
            b.address = post['business_address']

        except KeyError:
            raise ValidationError(_('Missing business info'), code='missing')

        except ValueError:
            raise ValidationError(_('Non-number business size'), code='badsize')

        e.save()
        b.employer = e
        b.save()
        self.business = b

        # Get subteam info
        if self.business.is_parent:
            # Create sector for subteams
            s = EmplSector()
            name = self.business.name
            s.name = ' '.join(name, '(by department)')
            s.parent = name
            s.save()

            # Get number of subteams
            try:
                num_subteams = int(post['num_subteams'])
            except ValueError:
                delete_objects(e, b, s)
                raise ValidationError(_('Invalid number of subteams.'), \
                    code='bad_num_subteam')

            # Create an Employer object for each subteam
            subteams = []
            for i in xrange(num_subteams):
                try:
                    t = Employer()
                    t.name = post['subteam_name_' + str(i)]
                    t.nr_employees = int(post['subteam_size_' + str(i)])
                    t.active = True
                    size_cat = size_category_id(t.nr_employees)
                    t.size_cat = EmplSizeCategory.objects.get(id=size_cat)
                    t.sector = s
                    subteams.append(t)
                except KeyError:
                    raise ValidationError(_('Subteam information missing'), \
                        code='missing_subteam')
                except ValueError:
                    raise ValidationError(_('Invalid subteam size'), \
                        code='bad_size')
                # Save subteams to database
                for t in subteams:
                    t.save()
                self.subteams = subteams

    def save_contact(self, post):

        # Get contact info
        try:
            self.contact = {
                'name': post['contact_name'],
                'title': post['contact_title'],
                'email': post['contact_email'],
                'phone': post['contact_phone']
            }
        except KeyError:
            print 'Contact Error'


    def display(self):
        return json.dumps(self.post, indent=2)
