from django import forms
from django.forms import ModelForm, HiddenInput

from survey.models import Commutersurvey, Employer, Team, Leg
from django.forms.models import inlineformset_factory

class CommuterForm(ModelForm):
  class Meta:
      model = Commutersurvey
      fields = ['name', 'email', 'share', 'home_address', 'work_address']

  # provides a dropdown list of active employers
  employer = forms.ModelChoiceField(queryset=Employer.objects.filter(active2015=True))

  # provides a dropdown list of teams
  team = forms.ModelChoiceField(queryset=Team.objects.filter(company__active2015=True))

  def __init__(self, *args, **kwargs):
      super(CommuterForm, self).__init__(*args, **kwargs)

      # add CSS classes and data attributes onto the generated form elements for bootstrap-material-design to play with
      self.fields['name'].widget.attrs['class'] = 'form-control'
      self.fields['email'].widget.attrs['class'] = 'form-control'
      self.fields['email'].widget.attrs['data-hint'] = 'A valid email should contain an @ symbol'
      self.fields['home_address'].widget.attrs['class'] = 'form-control'
      self.fields['home_address'].widget.attrs['data-hint'] = 'Use the address for the place you live during the work week.'
      self.fields['work_address'].widget.attrs['class'] = 'form-control'
      self.fields['work_address'].widget.attrs['data-hint'] = 'Use the address for your office, even if you telecommute.'
      self.fields['employer'].widget.attrs['class'] = 'form-control'
      self.fields['team'].widget.attrs['class'] = 'form-control'
      self.fields['team'].required = False
    
class LegForm(ModelForm):

  # creates a form using fields from the Leg model
  class Meta:
    model = Leg
    fields = ['direction', 'day', 'transport_mode', 'duration']

  def __init__(self, *args, **kwargs):
      super(LegForm, self).__init__(*args, **kwargs)

      # add CSS classes and data attributes onto the generated form elements for bootstrap-material-design to play with
      self.fields['transport_mode'].widget.attrs['class'] = 'form-control'
      self.fields['duration'].widget.attrs['class'] = 'form-control'
      self.fields['direction'].widget.attrs['class'] = 'form-control'
      self.fields['day'].widget.attrs['class'] = 'form-control'

MakeLegs = inlineformset_factory(Commutersurvey, Leg, form=LegForm, can_delete=False, extra=5)

