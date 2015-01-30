from django.db import models
from survey.models import Employer, EmplSector

from django.utils import timezone

from registration import Registration

class Questions(models.Model):
    heard_about = models.TextField()
    goals = models.TextField()
    sponsor = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Questions"


class Business(models.Model):
    """
    Business model, effectively an extension of the Employer model
    (which doesn't save any info about their website or address)
    """
    website = models.URLField(null=True, blank=True)
    address = models.TextField()
    employer = models.ForeignKey(Employer)

    class Meta:
        verbose_name_plural = "Businesses"

    def approve(self):
        self.employer.active = True

    @property
    def name(self):
        return self.employer.name

    @property
    def nr_employees(self):
        return self.employer.nr_employees

    @property
    def has_subteams(self):
        return self.employer.is_parent

    @property
    def subteams(self):
        """
        Returns a list of subteams (Employer object/models)
        If the business doesn't have subteams, returns an empty string
        """
        if self.has_subteams:
            sector = EmplSector.objects.get(parent=self.name)
            subteams = Employer.objects.filter(sector=sector.id)
            return subteams
        else:
            return []

    @property
    def num_subteams(self):
        return len(self.subteams)

    @property
    def subteam_names(self):
        """
        Returns a string of comma-separated subteam names
        (if business has subteams)

        If the business doesn't have any subteams, returns an empty string
        """
        if self.has_subteams:
            return ', '.join((subteam.name for subteam in self.subteams))
        else:
            return ''

class Contact(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    applied = models.DateTimeField(auto_now_add=True)
    questions = models.ForeignKey(Questions)
    business = models.ForeignKey(Business)

    @property
    def phone_number(self):
        """ pretty print for phone numbers """
        l = len(self.phone)
        if 10 <= l < 15:
            p = self.phone
            phone_string = ['(', p[-10:-7], ') ', p[-7:-4], '-', p[-4:]]
            if l > 10:
                phone_string = ['+',p[:-10] , ' '] + phone_string
            return ''.join(phone_string)
        else:
            return self.phone

    @property
    def fee(self):
        size = self.business.nr_employees
        num_subteams = self.business.num_subteams
        registration_date = self.applied
        return Registration.fee(size, num_subteams, registration_date)

    @property
    def business_name(self):
        return self.business.name
