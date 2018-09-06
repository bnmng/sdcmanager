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
        widgets = {
            'birth_date': forms.DateInput(attrs={'data-fieldtype': 'date'}),
        }

        localized_fields = ('birth_date',)
        

## Person owned Models (12m) ##

class VoxForm(ModelForm):
    class Meta:
        model = Vox
        fields=[
            'number',
            'primary',
            'restrict',
            'notes',
        ]
        widgets = {
            'number': forms.DateInput(attrs={'data-fieldtype': 'phone'}),
        }

class TxtmsgForm(ModelForm):
    class Meta:
        model = Txtmsg
        fields=[
            'number',
            'primary',
            'restrict',
            'notes',
        ]
        widgets = {
            'number': forms.DateInput(attrs={'data-fieldtype': 'phone'}),
        }

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
    class Meta:
        model = Application
        fields = (
            "person",
            "date_submitted",
            "image",
        )
        widgets = {
            'date_submitted': forms.DateInput(attrs={'data-fieldtype': 'date'}),
        }


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
