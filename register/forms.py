import json

from register.models import Questions, Business, Contact
from survey.models import Employer, EmplSector, EmplSizeCategory

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.core.validators import URLValidator, validate_email

import registration

def size_category_id(size):
    if size > 2000:
        return 4
    elif size > 300:
        return 3
    elif size > 51:
        return 2
    else:
        return 1

def invalid_size(s, length):
    return False if len(s) < length else True

class Form(object):
    """
    Django does have built in support for forms,
    """

    def __init__(self, post):
        """

        The order in which you save the models is important!
        """
        self.post = post
        self.save_questions(post)
        self.save_business(post)
        self.save_contact(post)

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
            e.active = False
            size_cat = size_category_id(e.nr_employees)
            e.size_cat = EmplSizeCategory.objects.get(id=size_cat)
            if 'has_subteams' in post:
                e.is_parent = True if post['has_subteams'] == 'true' else False

            # Get Business model data from form
            if 'business_website' in post:
                b.website = post['business_website']
                URLValidator(b.website)
            b.address = post['business_address']

        except KeyError:
            raise ValidationError(_('Missing business info'), code='missing')

        except ValueError:
            raise ValidationError(_('Non-number business size'), code='badsize')

        self.validate_employer(e)
        e.save()
        b.employer = e
        b.save()
        self.business = b

        # Get subteam info
        if self.business.employer.is_parent:
            # Create sector for subteams
            s = EmplSector()
            name = self.business.name
            s.name = ' '.join([name, '(by department)'])
            s.parent = name
            s.save()

            # Get number of subteams
            try:
                num_subteams = int(post['num_subteams'])
            except ValueError:
                for o in (s, b, e):
                    try:
                        o.delete()
                    except:
                        print 'Problem deleting', o
                raise ValidationError(_('Invalid number of subteams.'), \
                    code='bad_num_subteam')

            # Create an Employer object for each subteam
            subteams = []
            for i in xrange(num_subteams):
                try:
                    t = Employer()
                    t.name = post['subteam_name_' + str(i)]
                    t.nr_employees = int(post['subteam_size_' + str(i)])
                    # t.active = True
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
                for team in subteams:
                    team.save()
                self.subteams = subteams

    @staticmethod
    def validate_employer(e):
        """ Partial validation of Employer model """
        if invalid_size(e.name, 200):
            raise ValidationError(_('Business name is too long.'), \
                code='business_name_too_long')

        if type(e.nr_employees) != int:
            raise ValidationError(_('Business size must be an integer.'), \
                code='business_size_not_int')

    def save_contact(self, post):
        c = Contact()
        try:
            c.name = post['contact_name']
            c.title = post['contact_title']
            c.email = post['contact_email']
            phone = post['contact_phone']
            formatless_phone = ''.join(c for c in phone if c.isdigit())
            c.phone = formatless_phone
        except KeyError:
            raise ValidationError(_('Missing contact information.'), \
                code='contact_missing')

        c.questions = self.questions
        c.business = self.business
        self.validate_contact(c)
        c.save()
        self.contact = c

    @staticmethod
    def validate_contact(contact):
        validate_email(contact.email)

        if invalid_size(contact.phone, 15):
            raise ValidationError(_('Invalid phone number.'), \
                code='bad_phone')

        if invalid_size(contact.name, 200):
            raise ValidationError(_('Name is too long.'), \
                code='contact_name_too_long')

        if invalid_size(contact.title, 200):
            raise ValidationError(_('Title is too long.'), \
                code='contact_title_too_long')

    def display(self):
        return json.dumps(self.post, indent=2)

    @property
    def fee(self):
        """ Returns price of registration in $ """
        return self.contact.fee

    @property
    def business_has_subteams(self):
        return self.business.has_subteams
