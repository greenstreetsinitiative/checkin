from django.contrib.gis.db import models
from django.db.models import permalink
from django.utils.text import slugify
from django.db.models import Sum

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

class MonthManager(models.Manager):
    def active_months(self):
        return super(MonthManager, self).get_queryset().filter(active=True).order_by('-wr_day')

    def active_months_list(self):
        qs = self.active_months()
        return [am.month for am in self.active_months()]

class Month(models.Model):
    active = models.BooleanField()
    wr_day = models.DateField('W/R Day Date', null=True)
    open_checkin = models.DateField(null=True)
    close_checkin = models.DateField(null=True)

    objects = MonthManager()

    def __unicode__(self):
        return self.wr_day.strftime('%B %Y')

    class Meta:
        ordering = ['wr_day']

    @property
    def month(self):
        return self.wr_day.strftime(u'%B %Y'.encode('utf-8')).decode('utf-8')

    @property
    def url_month(self):
        return slugify(self.month)

    @property
    def short_name(self):
        return self.wr_day.strftime(u'%b\' %y'.encode('utf-8')).decode('utf-8')

    @property
    def wr_day_humanized(self):
        return self.wr_day.strftime('%A, %B %d, %Y')


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

class Team(models.Model):
  name = models.CharField("Team", max_length=100)
  company = models.ForeignKey('Employer', null=True, blank=True)

  def __str__(self):
    return self.name

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
    def carbon_diff(self):
        return Commutersurvey.objects.filter(employer=self).annotate(Sum('carbon_change')).values()

    @property
    def teams(self):
        return Team.objects.filter(employer=self)

    @property
    def nr_surveys(self):
        return Commutersurvey.objects.filter(employer=self).count()

    @property
    def nr_participants(self):
        return Commutersurvey.objects.filter(employer=self).distinct('email','name').count()

    def get_surveys(self, month):
        if self.is_parent:
            sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name))
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps)
            else:
                return Commutersurvey.objects.filter(month__in=Month.objects.active_months_list(), employer__in=sectorEmps)
        else:
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer=self)
            else:
                return Commutersurvey.objects.filter(month__in=Month.objects.active_months_list(), employer=self)

    def get_nr_surveys(self, month):
        if self.is_parent:
            sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name)).values_list('name', flat=True)
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps).count()
            else:
                return Commutersurvey.objects.filter(month__in=Month.objects.active_months_list(), employer__in=sectorEmps).count()
        else:
            if month != 'all':
                return Commutersurvey.objects.filter(month=month, employer__exact=self.name).count()
            else:
                return Commutersurvey.objects.filter(month__in=Month.objects.active_months_list(), employer__exact=self.name).count()

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

    # TODO: legacy field, remove it, requires leaderboard refactoring
    month = models.CharField('Walk/Ride Day Month', max_length=50)
    wr_day_month = models.ForeignKey(Month)

    home_address = models.CharField(max_length=200)
    work_address = models.CharField(max_length=200)

    geom = models.MultiLineStringField('Commute', geography=True, blank=True, null=True)

    distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)


    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    share = models.BooleanField('Don\'t share', default=False, help_text='Please do not share my identifying information with my employer.')
    employer_legacy = models.CharField(max_length=100, blank=True, null=True)
    employer = models.ForeignKey(Employer, null=True)
    # team = models.ForeignKey(Team, null=True, blank=True, default='')
    comments = models.TextField(null=True, blank=True)

    ip = models.IPAddressField('IP Address', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # optional survey questions
    health = models.IntegerField('Health condition', null=True, blank=True, choices=HEALTH_CHOICES)
    weight = models.CharField(null=True, blank=True, max_length=20)
    height = models.CharField(null=True, blank=True, max_length=20)
    gender = models.CharField(null=True, blank=True, max_length=1, choices=GENDER_CHOICES)
    gender_other = models.CharField(null=True, blank=True, max_length=50)
    cdays = models.IntegerField('last week to work: car', null=True, blank=True)
    caltdays = models.IntegerField('last week to work: alt. vehicle', null=True, blank=True)
    cpdays = models.IntegerField('last week to work: carpool', null=True, blank=True)
    tdays = models.IntegerField('last week to work: transit', null=True, blank=True)
    bdays = models.IntegerField('last week to work: bike', null=True, blank=True)
    rdays = models.IntegerField('last week to work: run', null=True, blank=True)
    wdays = models.IntegerField('last week to work: walk', null=True, blank=True)
    odays = models.IntegerField('last week to work: other', null=True, blank=True)
    tcdays = models.IntegerField('last week to work: telecommute', null=True, blank=True)
    lastweek = models.BooleanField('last week, same modes from work', default=True)
    cdaysaway = models.IntegerField('last week from work: car', null=True, blank=True)
    caltdaysaway = models.IntegerField('last week from work: alt. vehicle', null=True, blank=True)
    cpdaysaway = models.IntegerField('last week from work: carpool', null=True, blank=True)
    tdaysaway = models.IntegerField('last week from work: transit', null=True, blank=True)
    bdaysaway = models.IntegerField('last week from work: bike', null=True, blank=True)
    rdaysaway = models.IntegerField('last week from work: run', null=True, blank=True)
    wdaysaway = models.IntegerField('last week from work: walk', null=True, blank=True)
    odaysaway = models.IntegerField('last week from work: other', null=True, blank=True)
    tcdaysaway = models.IntegerField('last week from work: telecommute', null=True, blank=True)
    outsidechanges = models.TextField('mode change outside of work commute', null=True, blank=True)
    affectedyou = models.TextField('Other effects', null=True, blank=True)
    contact = models.BooleanField(default=False)
    volunteer = models.BooleanField('Available to volunteer', default=False)

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

        # Leg.objects.bulk_create([Leg(commutersurvey=self, **l) for l in legs])
        ###### won't call the leg save method

        # switch = self.switch_analysis()
        # self.from_work_switch = switch['fw']
        # self.to_work_switch = switch['tw']

        for l in legs:
            # creates the leg object, associates it with this commute, returns newly created leg
            obj = self.leg_set.create(**l)


        super(Commutersurvey, self).save(*args, **kwargs)

    def calculate_carbon_and_calories(self):
        legs = self.leg_set.all()

        difference = {'carbon': 0.000, 'calories': 0.000 }

        for leg in legs:
            if leg.day == 'w':
                difference["carbon"] += leg.carbon
                difference["calories"] += leg.calories
            elif leg.day == 'n':
                difference["carbon"] -= leg.carbon
                difference["calories"] -= leg.calories

        return difference

    carbon_change = models.FloatField(blank=True, null=True, default=0.0)
    calorie_change = models.FloatField(blank=True, null=True, default=0.0)

    CHANGE_CHOICES = (
        ('p', _('Positive change')),
        ('g', _('Green change')),
        ('h', _('Healthy change')),
        ('n', _('No change')),
    )

    change_type = models.CharField('Type of change', max_length=1, null=True, blank=True, choices=CHANGE_CHOICES)

    def change_analysis(self):
        if self.carbon_change < 0:
            if self.calorie_change > 0:
                return 'p' # positive change!
            else:
                return 'g' # green change
        else:
            if self.calorie_change > 0:
                return 'h' # healthy change
            else:
                return 'n' # no change

    already_green = models.BooleanField(default=False)

    def check_green(self):
        if self.leg_set.filter(day='n',new_mode__green=True).exists():
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        # backward compatibility
        self.month = self.wr_day_month.month

        changes = self.calculate_carbon_and_calories()
        self.carbon_change = changes["carbon"]
        self.calorie_change = changes["calories"]
        self.change_type = self.change_analysis()
        self.already_green = self.check_green()

        super(Commutersurvey, self).save(*args, **kwargs)

    @property
    def legs(self):
        return self.leg_set.all()

    def _active_months():
        return Month.objects.active_months().exclude(open_checkin__gt=date.today())

    def active_months():
        months = _active_months().values_list('id', flat=True)
        return (min(months), max(months))

    def get_surveys(employer_id=None, months=None):
        surveys = Commutersurvey.objects.all()
        # Filter out months
        if months and isinstance(months, int):
            surveys = surveys.filter(wr_day_month_id=months)
        elif months:
            min_month, max_month = months
            surveys = surveys.filter(wr_day_month__gte=min_month, wr_day_month__lte=max_month)
        # Filter out employer (accounts for subteams)
        if employer_id:
            employer = Employer.objects.get(id=employer_id)
            if employer.is_parent:
                # I can't use a get here because I can't guarantee that we'll
                # never get duplicate sector names, so I have to filter and get
                # the first element instead
                sector = EmplSector.objects.filter(parent=employer.name)[0]
                subteams = Employer.objects.filter(sector=sector)
                surveys = surveys.filter(employer__in=subteams)
            else:
                surveys = surveys.filter(employer_id=employer_id)
        return surveys

    def get_legs(employer_id=None, months=None):
        surveys = get_surveys(employer_id, months)
        legs = Leg.objects.filter(commutersurvey_id=surveys)
        return legs




class Mode(models.Model):
  mode = models.CharField("Mode", max_length=35)
  met = models.FloatField(blank=True, null=True)
  carb = models.FloatField(blank=True, null=True)
  speed = models.FloatField(blank=True, null=True)
  green = models.BooleanField(default=False)

  def __str__(self):
    return self.mode

class Leg(models.Model):
    """
    A leg (part) of a commute. One commute can be composed of multiple legs of
    different transportation modes.
    """

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

    new_mode = models.ForeignKey(Mode)
    mode = models.CharField(blank=True, null=True, max_length=4, choices=COMMUTER_MODES)
    direction = models.CharField(blank=True, null=True, max_length=2, choices=LEG_DIRECTIONS)
    duration = models.IntegerField(blank=True, null=True, choices=LEG_DURATIONS)
    day = models.CharField(blank=True, null=True, max_length=1, choices=LEG_DAYS)
    commutersurvey = models.ForeignKey(Commutersurvey)
    carbon = models.FloatField(blank=True, null=True, default=0.0)
    calories = models.FloatField(blank=True, null=True, default=0.0)

    def calc_calories(self):

        c = float(self.new_mode.met) # kcal/(kg*hour) from this mode

        calories = 0.0

        if c > 0.0:

            m = (self.duration * 15) - 7.5 # estimated minutes spent on leg
            if m < 0 : m = 0

            # amount of calories (kcal) burned by this leg using average American weight of 81 kg
            calories = c * (m/60) * 81

        return calories


    def calc_carbon(self):

        c = float(self.new_mode.carb) # grams carbon dioxide per passenger-mile on this mode

        carbon = 0.0

        if c > 0.0:

            s = float(self.new_mode.speed) # average speed of this mode in mph

            m = (self.duration * 15) - 7.5 # estimated minutes spent on leg
            if m < 0 : m = 0

            # amount of carbon in kilograms expended by this leg
            carbon = (c/1000) * s * (m/60)

        return carbon

    def save(self, *args, **kwargs):
        # save carbon change
        self.carbon = self.calc_carbon()
        self.calories = self.calc_calories()
        super(Leg, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Leg')
        verbose_name_plural = _('Legs')

    def __unicode__(self):
        return u'%s' % (self.mode)


