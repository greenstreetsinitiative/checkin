from django.contrib.gis.db import models
from django.db.models import permalink
from django.utils.text import slugify
from leaderboard.models import getMonths, Month

# lazy translation
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple

# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiLineStringField'])
except ImportError:
    pass


COMMUTER_MODES = (
    ('c', _('Car')),
    ('w', _('Walk')),
    ('b', _('Bike')),
    ('cp', _('Carpool')),
    ('t', _('Transit (bus, subway, etc.)')),
    ('o', _('Other (skate, canoe, etc.)')),
    ('tc', _('Telecommuting')),
)

LEG_DIRECTIONS = (
    ('tw', _('to work')),
    ('fw', _('from work')),
)

LEG_DAYS = (
    ('w', _('Walk/Ride Day')),
    ('n', _('Normal day')),
)

LEG_DURATIONS = (
    (1, _('Less than 15 minutes')),
    (2, _('15-30 minutes')),
    (3, _('30-45 minutes')),
    (4, _('45-60 minutes')),
    (5, _('More than an hour')),
)


class EmplSizeCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Employer Size Category')
        verbose_name_plural = _('Employer Size Categories')

    def __unicode__(self):
        return self.name

class EmplSector(models.Model):
    name = models.CharField(max_length=100)
    parent = models.CharField(max_length=100, default=None, null=True, blank=True)
    class Meta:
        verbose_name = _('Employer Sector')
        verbose_name_plural = _('Employer Sectors')

    @property 
    def url_name(self):
        return slugify(self.name)
    def __unicode__(self):
        return self.name

def makeParent(empName):
    emp = Employer.objects.get(name=empName)
    emp.is_parent = True
    emp.save()

class Employer(models.Model):
    """ Greens Streets Initiative Employer list """
    name = models.CharField("Employer name", max_length=200)
    nr_employees = models.IntegerField("Number of employees", null=True, blank=True)
    active = models.BooleanField("Show in Commuter-Form", default=False)
    size_cat = models.ForeignKey(EmplSizeCategory, null=True, blank=True, verbose_name=u'Size Category')
    sector = models.ForeignKey(EmplSector, null=True, blank=True)
    is_parent = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Employer')
        verbose_name_plural = _('Employers')
        ordering = ['name']

    def __unicode__(self):
        return self.name
    @property
    def nr_surveys(self):
        return Commutersurvey.objects.filter(employer__exact=self.name).count()

    def get_surveys(self, month):
        if self.is_parent:
            sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name)).values_list('name', flat=True)
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps)
            else:
                return Commutersurvey.objects.filter(month__in=getMonths(), employer__in=sectorEmps)
        else:
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__exact=self.name)
            else:
                return Commutersurvey.objects.filter(month__in=getMonths(), employer__exact=self.name)

    def get_nr_surveys(self, month):
        if self.is_parent:
            sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name)).values_list('name', flat=True)
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps).count()
            else:
                return Commutersurvey.objects.filter(month__in=getMonths(), employer__in=sectorEmps).count()
        else:
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__exact=self.name).count()
            else:
                return Commutersurvey.objects.filter(month__in=getMonths(), employer__exact=self.name).count()

    def get_new_surveys(self, month):
        monthObject = Month.objects.get(month=month)
        newSurveys = []
        previousMonths = monthObject.get_prior_months()
        for survey in Commutersurvey.objects.filter(month=month, employer=self.name):
            if not Commutersurvey.objects.filter(email=survey.email, month__in=previousMonths).exists():
                newSurveys += [survey,]
        return newSurveys

    def get_returning_surveys(self, month):
        monthObject = Month.objects.get(month=month)
        returningSurveys = []
        previousMonths = monthObject.get_prior_months()
        for survey in Commutersurvey.objects.filter(month=month, employer=self.name):
            if Commutersurvey.objects.filter(email=survey.email, month__in=previousMonths).exists():
                returningSurveys += [survey,]
        return returningSurveys


class Leg(models.Model):
    """
    A leg (part) of a commute. One commute can be composed of multiple legs of 
    different transportation modes.
    """

    mode = models.CharField(blank=True, null=True, max_length=2, choices=COMMUTER_MODES)
    direction = models.CharField(blank=True, null=True, max_length=2, choices=LEG_DIRECTIONS)
    duration = models.IntegerField(blank=True, null=True, choices=LEG_DURATIONS)
    day = models.CharField(blank=True, null=True, max_length=1, choices=LEG_DAYS)

    class Meta:
        verbose_name = _('Leg')
        verbose_name_plural = _('Legs')

    def __unicode__(self):
        return u'%s' % (self.mode) 
    

class Commutersurvey(models.Model):
    """
    Questions for adults about their commute work
    and Green Streets interest.
    """

    month = models.CharField('Walk/Ride Day Month', max_length=50)

    home_address = models.CharField(max_length=200)
    work_address = models.CharField(max_length=200)

    geom = models.MultiLineStringField('Commute', geography=True, blank=True, null=True)

    distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    legs = models.ManyToManyField(Leg)

    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    share = models.BooleanField(default=False)
    employer = models.CharField('Employer', max_length=100, blank=False, null=True)
    comments = models.TextField(null=True, blank=True)

    ip = models.IPAddressField('IP Address', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    weight = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)

    objects = models.GeoManager()

    CheckinDict = {
            ('c', 'c'):2, ('c', 'cp'):4, ('c', 'w'):4, ('c', 'b'):4, ('c', 't'):4, ('c', 'tc'):4, ('c', 'o'):1,
            ('cp', 'c'):1, ('cp', 'cp'):3, ('cp', 'w'):4, ('cp', 'b'):4, ('cp', 't'):4, ('cp', 'tc'):4, ('cp', 'o'):1,
            ('w', 'c'):1, ('w', 'cp'):3, ('w', 'w'):3, ('w', 'b'):3, ('w', 't'):3, ('w', 'tc'):3, ('w', 'o'):1,
            ('b', 'c'):1, ('b', 'cp'):3, ('b', 'w'):3, ('b', 'b'):3, ('b', 't'):3, ('b', 'tc'):3, ('b', 'o'):1,
            ('t', 'c'):1, ('t', 'cp'):3, ('t', 'w'):4, ('t', 'b'):4, ('t', 't'):3, ('t', 'tc'):4, ('t', 'o'):1,
            ('tc', 'c'):1, ('tc', 'cp'):3, ('tc', 'w'):3, ('tc', 'b'):3, ('tc', 't'):3, ('tc', 'tc'):3, ('tc', 'o'):1,
            ('o', 'c'):1, ('o', 'cp'):1, ('o', 'w'):1, ('o', 'b'):1, ('o', 't'):1, ('o', 'tc'):1, ('o', 'o'):1,
            }

    def __unicode__(self): 
        return u'%s' % (self.id)   

    class Meta:
        verbose_name = 'Commuter Survey'
        verbose_name_plural = 'Commuter Surveys'     

    # FIXME: migrate to multiple legs if still needed
    # @property
    # def to_work_switch(self):
    #     if self.to_work_today is None:
    #         self.to_work_today = 'o'
    #     if self.to_work_normally is None:
    #         self.to_work_normally = 'o'
    #     return self.CheckinDict[(self.to_work_normally, self.to_work_today)]

    # @property
    # def from_work_switch(self):
    #     if self.from_work_today is None:
    #         self.from_work_today = 'o'
    #     if self.from_work_normally is None:
    #         self.from_work_normally = 'o'
    #     return self.CheckinDict[(self.from_work_normally, self.from_work_today)]

