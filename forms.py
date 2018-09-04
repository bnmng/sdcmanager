from bnmng_widgets.widgets import AltClearableFileFieldWidget, CorrectingDateInput, CorrectingPhoneInput
from .models import Application, District, DistrictType, Email, Group, GroupMembership, Roster, RosterPlacement, Person, Residency, Txtmsg, Vox
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
import datetime 
import copy
from django.forms.widgets import CheckboxSelectMultiple
    
class PersonForm(ModelForm):
    birth_date=forms.DateField(widget=CorrectingDateInput)
    class Meta:
        model = Person
        fields = [
            'title',
            'first_name',
            'middle_names',
            'last_name',
            'suffixes',
            'prefered_name',
            'certificate_name',
            'letter_name',
            'birth_date',
            'voting_address',
            'mailing_address',
            'vfvid',
            'lcvid',
            'membershiptype',
        ]

        localized_fields = ('birth_date',)
        

## Person owned Models (12m) ##

class VoxForm(ModelForm):
    number=forms.CharField(widget=CorrectingPhoneInput)
    class Meta:
        model = Vox
        fields=[
            'number',
            'primary',
            'restrict',
            'notes',
        ]

class TxtmsgForm(ModelForm):
    number=forms.CharField(widget=CorrectingPhoneInput)
    class Meta:
        model = Txtmsg
        fields=[
            'number',
            'primary',
            'restrict',
            'notes',
        ]

class ResidencyForm(ModelForm):
    districttype_name = forms.CharField( required=False )
    class Meta:
        model = Residency
        fields =  '__all__'

class GroupMembershipForm(ModelForm):
    class Meta:
        model = GroupMembership
        fields = (
            "person",
            "group",
            "role_type",
            "role_name",
        )

class ApplicationForm(ModelForm):
    image=forms.ImageField(widget=AltClearableFileFieldWidget( attrs={'target': '_blank'}))
    date_submitted=forms.DateField(widget=CorrectingDateInput)
    class Meta:
        model = Application
        fields = (
            "person",
            "date_submitted",
            "image",
        )


class RosterPlacementForm(ModelForm):
    class Meta:
        model = RosterPlacement
        fields = (
            "person",
            "roster",
        )

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields='__all__'

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
            'grouptype'
        ]

class RosterForm(ModelForm):
    class Meta:
        model = Roster
        fields = '__all__'
