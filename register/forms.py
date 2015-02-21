import json
from datetime import datetime

from register.models import Questions, Business, Contact
from survey.models import Employer, EmplSector, EmplSizeCategory

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.core.validators import URLValidator, validate_email

import registration

validate_website = URLValidator(message='Please enter a valid website')

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
    Class to extract data from registration form and save it to the database

    Note: Django does have built in support for forms, but I wasn't sure how to
    handle the fact that you can have any number of subteams
    """

    def __init__(self, post):
        """
        Extracts data from POST request and saves them to the database
        Note: The order in which you save the models is important!
        """
        self.post = post
        try:
            self.save_business(post)
            self.save_questions(post)
            self.save_contact(post)
        except ValidationError as e:
            self.remove_from_db()
            raise e

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
            if not q.heard_about:
                 raise ValidationError(_('Please answer the question about \
                    how you heard about Walk/Ride Day'), \
                    code='missing_question')
            if 'wr_goals' in post:
                q.goals = post['wr_goals']
            if 'wr_sponsor' in post:
                q.sponsor = post['wr_sponsor']
            if 'wr_invoice' in post:
                q.invoice = post['wr_invoice']
        except KeyError:
            raise ValidationError(_('Missing questions from the bottom \
                of the form'), code='missing_question')
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
            if not e.name:
                raise ValidationError(_('Business name is missing'), \
                    code='missing')
            e.nr_employees = int(float(post['business_size']))
            e.active = False
            size_cat = size_category_id(e.nr_employees)
            e.size_cat = EmplSizeCategory.objects.get(id=size_cat)
            if 'has_subteams' in post:
                e.is_parent = True if post['has_subteams'] == 'true' else False

            # Get Business model data from form
            if 'business_website' in post and post['business_website']:
                b.website = post['business_website']
                if 'http' not in b.website:
                    url = 'http://' + b.website
                else:
                    url = b.website
                validate_website(url)
    
            b.address = post['business_address']

        except KeyError:
            raise ValidationError(_('Missing business info'), code='missing')

        except ValueError:
            raise ValidationError(_('Missing or invalid business size'),
                code='badsize')

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
                raise ValidationError(_('Please enter a valid number of subteams.'), code='bad_num_subteam')

            # Create an Employer object for each subteam
            subteams = []
            for i in xrange(num_subteams):
                try:
                    t = Employer()
                    t.name = post['subteam_name_' + str(i)]
                    t.nr_employees = int(post['subteam_size_' + str(i)])
                    size_cat = size_category_id(t.nr_employees)
                    t.size_cat = EmplSizeCategory.objects.get(id=size_cat)
                    t.sector = s
                    subteams.append(t)
                except KeyError:
                    raise ValidationError(_('Some subteam information is missing'), code='missing_subteam')
                except ValueError:
                    raise ValidationError(_('Please enter a valid subteam size'), code='bad_size')
                # Save subteams to database
                for team in subteams:
                    team.save()
            self.subteams = subteams

    @staticmethod
    def validate_employer(e):
        """ Partial validation of Employer model """
        if invalid_size(e.name, 200):
            raise ValidationError(_('Please limit business name to 200 characters'),
                code='business_name_too_long')

        if type(e.nr_employees) != int:
            raise ValidationError(_('Please enter a valid number for the size'),
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
            raise ValidationError(_('Please enter all contact information.'), \
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
            raise ValidationError(_('Please enter a valid phone number'), \
                code='bad_phone')

        if invalid_size(contact.name, 200):
            raise ValidationError(_('Please limit the contact name to 200 characters'), code='contact_name_too_long')

        if invalid_size(contact.title, 200):
            raise ValidationError(_('Please limit the contact\'s title to 200 characters'), code='contact_title_too_long')

    @property
    def fee(self):
        """ Returns price of registration in $ """
        return self.contact.fee

    @property
    def business_has_subteams(self):
        return self.business.has_subteams

    def email(self):
        """ Representation of form to send as email """
        invoice = self.questions.invoice
        invoice = 'Yes\n' + invoice if invoice else 'No.'

        return ''.join([
            'Submitted: ', str(self.contact.applied), '\n',
            '\nBusiness:',
            '\nName: ', self.business.name,
            '\nSize: ', str(self.business.nr_employees),
            '\nNumber of subteams: ', str(self.business.num_subteams),
            '\nAddress: ', self.business.address,
            '\nWebsite: ', self.business.website,
            '\n\nContact:',
            '\nName: ', self.contact.name,
            '\nTitle: ', self.contact.title,
            '\nEmail: ', self.contact.email,
            '\nPhone: ', self.contact.phone,
            '\n\nQuestions:',
            '\nHow did you hear of the Walk/Ride Day Corporate Challenge?\n',
            self.questions.heard_about,
            "\n\nWhat are your goals and/or expecations from your organization's participation in this year's Challenge?\n",
            self.questions.goals,
            '\n\nWould you like to become a Green Streets sponsor by funding an intern, sponsoring an event, etc.?\n',
            self.questions.sponsor,
            '\n\nDo you require an invoice from Green Streets?\n',
            invoice,
            '\n\nTOTAL Registration Fee: $', str(self.contact.fee)
        ])

    def remove_from_db(self):
        """
        Removes all models associated with this form from the database
        Call this when you detect an error somewhere
        """
        if 'contact' in self.__dict__:
            self.contact.delete()

        # Need to delete emplsector, employer, and subteams
        if 'business' in self.__dict__:
            subteams = self.subteams
            if len(subteams) > 0:
                sector = subteams[0].sector
                sector.delete()
            for team in subteams:
                team.delete()
            employer = self.business.employer
            self.business.delete()
            employer.delete()

        if 'questions' in self.__dict__:
            self.questions.delete()
