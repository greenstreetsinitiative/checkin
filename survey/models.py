from __future__ import division
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

    @property
    def surveys(self):
        return self.commutersurvey_set.all()

class EmplSizeCategory(models.Model):
    SIZE_OPTIONS = (
        ('lg', _('Large')),
        ('md', _('Medium')),
        ('sm', _('Small')),
        ('xs', _('Very small')),
    )

    name = models.CharField(max_length=50)
    size_category = models.CharField('Size Category', max_length=2, null=True, blank=True, choices=SIZE_OPTIONS)

    @property
    def employers(self):
        return self.employer_set.all()

    class Meta:
        verbose_name = _('Employer Size Category')
        verbose_name_plural = _('Employer Size Categories')

    def __unicode__(self):
        return self.name

class Sector(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)

    @property
    def employers(self):
        return self.employer_set.all()

    class Meta:
        verbose_name = _('Employment Sector')
        verbose_name_plural = _('Employment Sectors')

    @property
    def url_name(self):
        return slugify(self.name)
    def __unicode__(self):
        return self.name


class Team(models.Model):
  name = models.CharField("Team", max_length=100)
  company = models.ForeignKey('Employer', null=True, blank=True)

  @property
  def surveys(self):
      return self.commutersurvey_set.all()

  def __str__(self):
    return self.name

class Employer(models.Model):
    """ Greens Streets Initiative Employer list """
    name = models.CharField("Employer name", max_length=200)
    nr_employees = models.IntegerField("Number of employees", null=True, blank=True)
    active = models.BooleanField("Show in Commuter-Form", default=False)
    size_cat = models.ForeignKey(EmplSizeCategory, null=True, blank=True, verbose_name=u'Size Category')
    sector = models.ForeignKey(Sector, null=True, blank=True)

    class Meta:
        verbose_name = _('Employer')
        verbose_name_plural = _('Employers')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def teams(self):
        return self.team_set.all()

    @property
    def surveys(self):
        return self.commutersurvey_set.all()

    @property
    def nr_already_green(self):
        return self.commutersurvey_set.filter(already_green=True).count()

    @property
    def nr_green_switches(self):
        return self.commutersurvey_set.filter(change_type='g').count()

    @property
    def nr_healthy_switches(self):
        return self.commutersurvey_set.filter(change_type='h').count()

    @property
    def nr_positive_switches(self):
        return self.commutersurvey_set.filter(change_type='p').count()

    @property
    def nr_participants(self):
        return self.commutersurvey_set.distinct('email', 'name').only('email','name').count()

class Commutersurvey(models.Model):
    """
    Questions for adults about their commute work
    and Green Streets interest.
    """
    wr_day_month = models.ForeignKey(Month)

    home_address = models.CharField(max_length=200)
    work_address = models.CharField(max_length=200)

    geom = models.MultiLineStringField('Commute', geography=True, blank=True, null=True)

    distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)


    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    share = models.BooleanField('Don\'t share', default=False, help_text='Please do not share my identifying information with my employer.')

    employer = models.ForeignKey(Employer, null=True)

    team = models.ForeignKey('Team', null=True, blank=True)

    comments = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)


    volunteer = models.BooleanField('Available to volunteer', default=False)

    objects = models.GeoManager()

    # filtered = SurveyFilterManager()

    def __unicode__(self):
        return u'%s' % (self.id)

    class Meta:
        verbose_name = 'Commuter Survey'
        verbose_name_plural = 'Commuter Surveys'
        ordering = ['created']


    def save_with_legs(self, *args, **kwargs):

        legs = kwargs['legs']
        del kwargs['legs']

        for l in legs:
            # creates the leg object, associates it with this commute, returns newly created leg
            obj = self.leg_set.create(**l)

        super(Commutersurvey, self).save(*args, **kwargs)

    def calculate_carbon_and_calories(self):
        legs = self.leg_set.only('carbon','calories','day').all()

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

    change_type = models.CharField('Type of change', max_length=1, null=True, blank=True)

    def change_analysis(self):
        if self.carbon_change < 0 and self.calorie_change > 0:
            return 'p' # positive change!

        elif self.carbon_change < 0:
            return 'g' # green change

        elif self.calorie_change > 0:
            return 'h' # healthy change

        else:
            return 'n' # no change

    already_green = models.BooleanField(default=False)

    def check_green(self):
        # if any leg on a normal day commute is green
        return self.leg_set.filter(day='n',mode__green=True).exists()

    def save(self, *args, **kwargs):

        # run calculations on save
        changes = self.calculate_carbon_and_calories()
        self.carbon_change = changes["carbon"]
        self.calorie_change = changes["calories"]
        self.change_type = self.change_analysis()
        self.already_green = self.check_green()

        super(Commutersurvey, self).save(*args, **kwargs)

    def _active_months():
        return Month.objects.active_months().exclude(open_checkin__gt=date.today())

    def active_months():
        months = _active_months().values_list('id', flat=True)
        return (min(months), max(months))


class Mode(models.Model):
  name = models.CharField(max_length=35)
  met = models.FloatField(blank=True, null=True)
  carb = models.FloatField(blank=True, null=True)
  speed = models.FloatField(blank=True, null=True)
  green = models.BooleanField(default=False)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

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

    commutersurvey = models.ForeignKey(Commutersurvey)
    day = models.CharField(blank=True, null=True, max_length=1, choices=LEG_DAYS)
    direction = models.CharField(blank=True, null=True, max_length=2, choices=LEG_DIRECTIONS)
    mode = models.ForeignKey(Mode, blank=True, null=True)
    duration = models.IntegerField("Time in minutes", blank=True, null=True)
    carbon = models.FloatField(blank=True, null=True, default=0.0)
    calories = models.FloatField(blank=True, null=True, default=0.0)

    def calc_metrics(self):
        calories = 0.0
        carbon = 0.0

        kcal = float(self.mode.met) # kcal/(kg*hour) from this mode

        if kcal > 0.0:
            # amount of calories (kcal) burned by this leg using average American weight of 81 kg based on a duration in minutes
            calories = kcal * (self.duration/60) * 81

        coo = float(self.mode.carb) # grams carbon dioxide per passenger-mile on this mode

        if coo > 0.0:

            s = float(self.mode.speed) # average speed of this mode in mph

            # amount of carbon in kilograms expended by this leg based on a duration in minutes
            carbon = (coo/1000) * s * (self.duration/60)

        return {'carbon': carbon, 'calories': calories }

    def save(self, *args, **kwargs):
        # save carbon change
        metrics = self.calc_metrics()
        self.carbon = metrics['carbon']
        self.calories = metrics['calories']
        super(Leg, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Leg')
        verbose_name_plural = _('Legs')


    def __unicode__(self):
        return u'%s' % (self.mode.name)


