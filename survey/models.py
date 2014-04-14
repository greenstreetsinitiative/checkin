from django.contrib.gis.db import models
from django.db.models import permalink
from django.utils.text import slugify

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
    ('cp', _('Carpool')),
    ('da', _('Driving alone')),
    ('dalt', _('Driving alone, alternative vehicle')),
    ('w', _('Walk')),
    ('b', _('Bike')),
    ('t', _('Transit (bus, subway, etc.)')),
    ('o', _('Other (skate, canoe, etc.)')),
    ('r', _('Jog/Run')),
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

HEALTH_CHOICES = (
    (5, _('Excellent')),
    (4, _('Very Good')),
    (3, _('Good')),
    (2, _('Fair')),
    (1, _('Poor')),
)

GENDER_CHOICES = (
    ('m', _('Male')),
    ('f', _('Female')),
    ('o', _('Other')),
)

class ActiveMonthManager(models.Manager):
    def get_queryset(self):
        return super(ActiveMonthManager, self).get_queryset().filter(active=True).order_by('-date')

class Month(models.Model):
    month = models.CharField(max_length=100)
    active = models.BooleanField()
    date = models.DateField()
    open_checkin = models.DateField(null=True)
    close_checkin = models.DateField(null=True)
    url_month = models.CharField(max_length=100, default='')
    short_name = models.CharField(max_length=50, default='')
    
    objects = models.Manager()
    active_months = ActiveMonthManager()

    def __unicode__(self):
        return self.month
    
    @property
    def prior_months(self):
        return self.objects.filter(id__lt=self.id).values_list('month', flat=True)


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
                return Commutersurvey.objects.filter(month__in=Month.active_months.values_list('month', flat=True), employer__in=sectorEmps)
        else:
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__exact=self.name)
            else:
                return Commutersurvey.objects.filter(month__in=Month.active_months.values_list('month', flat=True), employer__exact=self.name)

    def get_nr_surveys(self, month):
        if self.is_parent:
            sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name)).values_list('name', flat=True)
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps).count()
            else:
                return Commutersurvey.objects.filter(month__in=Month.active_months.values_list('month', flat=True), employer__in=sectorEmps).count()
        else:
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__exact=self.name).count()
            else:
                return Commutersurvey.objects.filter(month__in=Month.active_months.values_list('month', flat=True), employer__exact=self.name).count()

    def get_new_surveys(self, month):
        monthObject = Month.objects.get(month=month)
        newSurveys = []
        previousMonths = monthObject.prior_months
        for survey in Commutersurvey.objects.filter(month=month, employer=self.name):
            if not Commutersurvey.objects.filter(email=survey.email, month__in=previousMonths).exists():
                newSurveys += [survey,]
        return newSurveys

    def get_returning_surveys(self, month):
        monthObject = Month.objects.get(month=month)
        returningSurveys = []
        previousMonths = monthObject.prior_months
        for survey in Commutersurvey.objects.filter(month=month, employer=self.name):
            if Commutersurvey.objects.filter(email=survey.email, month__in=previousMonths).exists():
                returningSurveys += [survey,]
        return returningSurveys


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

    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    share = models.BooleanField(default=False)
    employer = models.CharField('Employer', max_length=100, blank=False, null=True)
    comments = models.TextField(null=True, blank=True)

    ip = models.IPAddressField('IP Address', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # optional survey questions
    health = models.IntegerField(null=True, blank=True, choices=HEALTH_CHOICES)
    weight = models.CharField(null=True, blank=True, max_length=20)
    height = models.CharField(null=True, blank=True, max_length=20)
    gender = models.CharField(null=True, blank=True, max_length=1, choices=GENDER_CHOICES)
    gender_other = models.CharField(null=True, blank=True, max_length=50)
    cdays = models.IntegerField(null=True, blank=True)
    caltdays = models.IntegerField(null=True, blank=True)
    cpdays = models.IntegerField(null=True, blank=True)
    tdays = models.IntegerField(null=True, blank=True)
    bdays = models.IntegerField(null=True, blank=True)
    rdays = models.IntegerField(null=True, blank=True)
    wdays = models.IntegerField(null=True, blank=True)
    odays = models.IntegerField(null=True, blank=True)
    tcdays = models.IntegerField(null=True, blank=True)
    lastweek = models.BooleanField(default=True)
    cdaysaway = models.IntegerField(null=True, blank=True)
    caltdaysaway = models.IntegerField(null=True, blank=True)
    cpdaysaway = models.IntegerField(null=True, blank=True)
    tdaysaway = models.IntegerField(null=True, blank=True)
    bdaysaway = models.IntegerField(null=True, blank=True)
    rdaysaway = models.IntegerField(null=True, blank=True)
    wdaysaway = models.IntegerField(null=True, blank=True)
    odaysaway = models.IntegerField(null=True, blank=True)
    tcdaysaway = models.IntegerField(null=True, blank=True)
    outsidechanges = models.TextField(null=True, blank=True)
    affectedyou = models.TextField(null=True, blank=True)
    contact = models.BooleanField(default=False)
    volunteer = models.BooleanField(default=False)

    objects = models.GeoManager()

    def __unicode__(self): 
        return u'%s' % (self.id)   

    class Meta:
        verbose_name = 'Commuter Survey'
        verbose_name_plural = 'Commuter Surveys'     

    def save_with_legs(self, *args, **kwargs):
        """
        Also creates related Commutersurvey legs
        """
        legs = kwargs['legs']
        del kwargs['legs']

        super(Commutersurvey, self).save(*args, **kwargs)

        for l in legs:
            print l
            leg = Leg(commutersurvey=self, **l)
            leg.save()

    @property
    def legs(self):
        return self.leg_set.all()

    @property
    def from_work_switch(self):
        normal_green_legs = 0
        wr_green_legs = 0
        for leg in self.legs:
            if leg.mode != 'c' and leg.mode != 'da' and leg.direction == 'fw' and leg.day == 'w':
                wr_green_legs += 1
            if leg.mode != 'c' and leg.mode != 'da' and leg.direction == 'fw' and leg.day == 'n':
                normal_green_legs += 1
        
        if wr_green_legs == 0:
            return 2 # car commute
        if wr_green_legs > normal_green_legs:
            return 4 # green switch
        if wr_green_legs < normal_green_legs:
            return 1 # "unhealthy switch"
        if wr_green_legs > 0:
            return 3 # green commute
    
    @property
    def to_work_switch(self):
        normal_green_legs = 0
        wr_green_legs = 0
        for leg in self.legs:
            if leg.mode != 'c' and leg.mode != 'da' and leg.direction == 'tw' and leg.day == 'w':
                wr_green_legs += 1
            if leg.mode != 'c' and leg.mode != 'da' and leg.direction == 'tw' and leg.day == 'n':
                normal_green_legs += 1
        
        if wr_green_legs == 0:
            return 2 # car commute
        if wr_green_legs > normal_green_legs:
            return 4 # green switch
        if wr_green_legs < normal_green_legs:
            return 1 # "unhealthy switch"
        if wr_green_legs > 0:
            return 3 # green commute


class Leg(models.Model):
    """
    A leg (part) of a commute. One commute can be composed of multiple legs of 
    different transportation modes.
    """

    mode = models.CharField(blank=True, null=True, max_length=2, choices=COMMUTER_MODES)
    direction = models.CharField(blank=True, null=True, max_length=2, choices=LEG_DIRECTIONS)
    duration = models.IntegerField(blank=True, null=True, choices=LEG_DURATIONS)
    day = models.CharField(blank=True, null=True, max_length=1, choices=LEG_DAYS)
    commutersurvey = models.ForeignKey(Commutersurvey)

    class Meta:
        verbose_name = _('Leg')
        verbose_name_plural = _('Legs')

    def __unicode__(self):
        return u'%s' % (self.mode) 
