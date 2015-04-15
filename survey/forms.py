from django import forms
from django.forms import ModelForm, HiddenInput

from survey.models import Commutersurvey, Employer, Team, Leg
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet

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

      # add CSS classes for bootstrap
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
      self.fields['email'].required = True
  
class RequiredFormSet(BaseInlineFormSet):
  def __init__(self, *args, **kwargs):
      super(RequiredFormSet, self).__init__(*args, **kwargs)
      for form in self.forms:
          form.empty_permitted = False

class LegForm1(ModelForm):

  class Meta:
    model = Leg
    fields = ['transport_mode', 'duration', 'day', 'direction']

  def __init__(self, *args, **kwargs):
      super(LegForm1, self).__init__(*args, **kwargs)

      self.fields['transport_mode'].widget.attrs['class'] = 'form-control'
      self.fields['duration'].widget.attrs['class'] = 'form-control'
      self.fields['transport_mode'].required = True
      self.fields['duration'].required = True
      self.fields['day'].initial = 'n'
      self.fields['direction'].initial = 'tw'
      self.fields['day'].widget = forms.HiddenInput()
      self.fields['direction'].widget = forms.HiddenInput()

class LegForm2(ModelForm):

  class Meta:
    model = Leg
    fields = ['transport_mode', 'duration', 'day', 'direction']

  def __init__(self, *args, **kwargs):
      super(LegForm2, self).__init__(*args, **kwargs)

      self.fields['transport_mode'].widget.attrs['class'] = 'form-control'
      self.fields['duration'].widget.attrs['class'] = 'form-control'
      self.fields['transport_mode'].required = True
      self.fields['duration'].required = True
      self.fields['day'].initial = 'n'
      self.fields['direction'].initial = 'fw'
      self.fields['day'].widget = forms.HiddenInput()
      self.fields['direction'].widget = forms.HiddenInput()

class LegForm3(ModelForm):

  class Meta:
    model = Leg
    fields = ['transport_mode', 'duration', 'day', 'direction']

  def __init__(self, *args, **kwargs):
      super(LegForm3, self).__init__(*args, **kwargs)

      self.fields['transport_mode'].widget.attrs['class'] = 'form-control'
      self.fields['duration'].widget.attrs['class'] = 'form-control'
      self.fields['transport_mode'].required = True
      self.fields['duration'].required = True
      self.fields['day'].initial = 'w'
      self.fields['direction'].initial = 'tw'
      self.fields['day'].widget = forms.HiddenInput()
      self.fields['direction'].widget = forms.HiddenInput()

class LegForm4(ModelForm):

  class Meta:
    model = Leg
    fields = ['transport_mode', 'duration', 'day', 'direction']

  def __init__(self, *args, **kwargs):
      super(LegForm4, self).__init__(*args, **kwargs)

      self.fields['transport_mode'].widget.attrs['class'] = 'form-control'
      self.fields['duration'].widget.attrs['class'] = 'form-control'
      self.fields['transport_mode'].required = True
      self.fields['duration'].required = True
      self.fields['day'].initial = 'w'
      self.fields['direction'].initial = 'fw'
      self.fields['day'].widget = forms.HiddenInput()
      self.fields['direction'].widget = forms.HiddenInput()

MakeLegs_NormalTW = inlineformset_factory(Commutersurvey, Leg, formset=RequiredFormSet, form=LegForm1, can_delete=False, extra=1, max_num=5)
MakeLegs_NormalFW = inlineformset_factory(Commutersurvey, Leg, formset=RequiredFormSet, form=LegForm2, can_delete=False, extra=1, max_num=5)
MakeLegs_WRTW = inlineformset_factory(Commutersurvey, Leg, formset=RequiredFormSet, form=LegForm3, can_delete=False, extra=1, max_num=5)
MakeLegs_WRFW = inlineformset_factory(Commutersurvey, Leg, formset=RequiredFormSet, form=LegForm4, can_delete=False, extra=1, max_num=5)

