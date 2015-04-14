from django import forms
from django.forms import ModelForm, HiddenInput

from survey.models import Commutersurvey, Employer, Team, Leg


class CommuterForm(ModelForm):
    class Meta:
        model = Commutersurvey
        fields = ['name', 'email', 'share', 'home_address', 'work_address', 'comments', 'contact', 'volunteer']
        exclude = ('walkrideday','ip')
        widgets = {
                   'home_location': HiddenInput(),
                   'work_location': HiddenInput(),
                   'distance': HiddenInput(),
                   'duration': HiddenInput(),
                   }

    # provides a dropdown list of active employers
    employer = forms.ModelChoiceField(queryset=Employer.objects.filter(active=True))

    # provides a dropdown list of teams
    team = forms.ModelChoiceField(queryset=Team.objects.all())

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
    
class LegForm(ModelForm):

  # creates a form using fields from the Leg model
  class Meta:
    model = Leg
    fields = ['transport_mode', 'duration', 'direction', 'day']

