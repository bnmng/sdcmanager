from django.db.models.functions import Greatest
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class DistrictType(models.Model):
    """
    Model representing the type of district ie Precinct, County, Congressional, etc.
    """
    name = models.CharField('Name', max_length=40, help_text='What is the name of this type of  district?')
    order = models.SmallIntegerField('Display Order', help_text='In what position should this appear on a list?')

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class District(models.Model):

    name = models.CharField('Name', max_length=40, help_text='What is the name of this district?')
    districttype = models.ForeignKey(DistrictType, on_delete=models.SET_NULL, null=True, help_text='What type of district is this?')
    van_id = models.CharField('VAN ID', max_length=30, blank=True, null=True, help_text='What is the VAN id for this district?')

    class Meta:
        ordering = ['districttype', 'name']

    def __str__(self):
        return self.name

class EventType(models.Model):
    """
    Model representing the type of event ie Precinct, County, Congressional, etc.
    """
    name = models.CharField('Name', max_length=40, help_text='What is the name of this type of event?')
    order = models.SmallIntegerField('Display Order', help_text='In what position should this display (low numbers first by default)?')

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Event(models.Model):

    name = models.CharField('Name', max_length=40, help_text='What is the name of this event?')
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, help_text='What type of event is this?')
    

    class Meta:
        ordering = ['event_type', 'name']

    def __str__(self):
        return '{0}: {1}'.format(self.event_type, self.name)

class GroupType(models.Model):
    """
    Model representing the type of group ie Standing Committee, Committee, Work-Group, etc.
    """
    name = models.CharField('Name', max_length=40, help_text='What is the name of this type of group?')
    order = models.SmallIntegerField('Display Order', help_text='Where should groups of this type display on lists (low numbers first by default)?')

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Group(models.Model):

    name = models.CharField('Name', max_length=40, help_text='What is the name of this group?')
    grouptype = models.ForeignKey(GroupType, on_delete=models.SET_NULL, null=True, blank=True, help_text='What type of group is this?')
    protect = models.BooleanField('Protect from Edit', default=False, help_text='Should this group be protected from edits and deletions from non-staff users?')
    parent = models.ForeignKey('self', related_name='Child', on_delete=models.SET_NULL, blank=True, null=True, help_text='What is the parent of this group?')

    class Meta:
        ordering = ['grouptype__order', 'name']

    def get_absolute_url(self):
        return reverse('group-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
        return '{0}: {1}'.format(self.grouptype, self.name)

class MembershipType(models.Model):

    name = models.CharField('Name', max_length=40, help_text='What is the name of this status?')
    order = models.SmallIntegerField('Display Order', help_text='In what position should this display (low numbers first by default)?')
    counts_quorum = models.BooleanField('Counts as Quorum', help_text='Should people with this status and an appropriate membership type count towards a quorum?')

    def get_absolute_url(self):
        return reverse('membershipstype-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Roster(models.Model):

    name = models.CharField('Name', max_length=40, help_text='What is the name of this roster?')
    user = models.ForeignKey(User, related_name="roster_owner", on_delete=models.CASCADE, blank=True, null=True, help_text='To whom does this roster belong?')
    is_public = models.BooleanField('Share', help_text='Should other users have access to this roster?')

    class Meta:
        ordering = ['user', 'name']

    def get_absolute_url(self):
        return reverse('roster-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Person(models.Model):

    title = models.CharField('Title', max_length=12, blank=True, help_text='What is this person\'s abbreviated title (ie "Mr.", "Ms.", "Dr.", "Rev.")?')
    first_name = models.CharField('First Name', max_length=40, help_text='What is this person\'s first name?')
    middle_names = models.CharField('Middle Names or Initials', blank=True, max_length=40, help_text='What are this person\'s middle names or middle initials (whichever is prefered)?')
    last_name = models.CharField('Family Name', max_length=40, blank=True,  help_text='What is this person\'s last name?')
    suffixes = models.CharField('Suffixes', max_length=12, blank=True, help_text='What are this  person\'s suffixes (ie "Sr.", "III", "Esq." )?')

    prefered_name = models.CharField('Prefered Name', max_length=40, blank=True, help_text='By what name would this person prefer to be called (ie "Ray")?')
    certificate_name = models.CharField('Name for Certificates', max_length=75, blank=True, help_text='How should this person\'s name appear on a certificate?')
    letter_name = models.CharField('Name for Letters', max_length=50, blank=True, help_text='How should this name appear in a letter (after "Dear") ( ie "Ms. Smith")?')

    birth_date = models.DateField('Date of Birth', null=True, blank=True, help_text='When was this person born?')

    voting_address = models.TextField('Voting Address', max_length=1000, blank=True, help_text='What is this person\'s voting address?')
    mailing_address = models.TextField('Mailing Address', max_length=1000, blank=True, help_text='What is this person\'s mailing address?')

    vfvid = models.CharField('Voter File Van ID', max_length=20, blank=True, help_text='What is this person\'s voter File VAN ID?')
    lcvid = models.CharField('Local Van ID', max_length=20, blank=True, help_text='What is this person\'s local VAN ID (aka My Campaign ID)?')

    membershiptype = models.ForeignKey(MembershipType, on_delete=models.PROTECT, blank=True, null=True, help_text='What is the type of this person\'s membership?')

    def list_groups(self):
        return ', '.join([ '{0}: {1}'.format( group.type, group.name ) for district in group_set.all() ] )
    
    list_groups.short_description = 'Groups'

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_names']

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])

    def __str__(self):
        if self.prefered_name is not None and self.prefered_name > '':
            prefered_name = '(' + self.prefered_name + ')'
        else:
            prefered_name = ''

        full_name = (self.first_name + prefered_name + self.last_name)

        if full_name > '':
            return full_name
        return "Un-named Person"

            
class Application(models.Model):

    date_submitted = models.DateField('Date Submitted', null=True, blank=True, help_text='When was this application was submitted?' )
    image = models.ImageField('Image', upload_to='applications', help_text='What is the image for this application?')

    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='For which person is this application?')

    def __str__(self):
        return str(self.date_submitted)

class PaymentMethod(models.Model):

    name = models.CharField('Name', max_length=40, help_text='What is the name of the type of payment?')

    def __str__(self):
        return str(self.name)
    
class Dues(models.Model):

    date_effective = models.DateField('Effective Date', help_text='What is the effective date of the payment?  This may be different (often later) than the actual date of payment.' )
    date_checked = models.DateField('Check or Transaction Date', blank=True, null=True, help_text='What is the date on the check or the date of electronic transfer if applicable?  This is used for helping with locating the payment information')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, help_text='What method was used for this payment?')

    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='For which person was this dues payed?')

    def __str__(self):
        return str(self.date_submitted)

class Email(models.Model):

    address = models.CharField('Email Address', max_length=40, help_text='What is this person\'s email address?')
    primary = models.BooleanField('Primary', help_text='Is this the primary email address?')
    restrict = models.BooleanField('Restrict Use', help_text='Should this email address not be used for email lists and automated emails?')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='For which person is this email account?')

    def __str__(self):
        return self.person + ': ' + self.address 

    class Meta:
        ordering = ('restrict', '-primary', 'address')

class GroupMembership(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE, help_text='What is the group of which the person is a member?')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Who is the person who is a member of this group?')
    ROLE_TYPE_CHOICES=( 
        ('', 'Unknown or N/A'),
        ('aA', 'Member'),
        ('4O', 'Officer'),
        ('2L', 'Chairperson'),
    )
    role_type = models.CharField('Role Type', max_length=2,  blank=True, null=True, help_text='What type of role does this person hold in the group?', choices=ROLE_TYPE_CHOICES)
    role_name = models.CharField('Role Name', max_length=40, blank=True, null=True, help_text='What is the name of the role that the person holds in the group? This can be left blank, in which case the role type will be used.')

    class Meta:
        ordering = ['group__grouptype__order', 'role_type', 'person']

    def __str__(self):
        if self.role_type > '':
            return self.event + ': ' + self.person + ': ' + self.role_type
        return self.event + ': ' + self.person 

class Txtmsg(models.Model):

    number = models.CharField('Number', max_length=30, help_text='What is this person\'s text number?')
    primary = models.BooleanField('Is Primary', help_text='Is this the primary text number?')
    restrict = models.BooleanField('Restrict Use', help_text='Should this number not be used for text lists and automated texts?')
    notes = models.CharField('Notes', max_length=255, blank=True, help_text='What are some important notes about this text number? ')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='For which person is this messaging device?')

    def __str__(self):
        return self.person + ': ' + self.number 

    class Meta:
        verbose_name = "Txtmsg"
        ordering = ['restrict', '-primary', 'number']

class Vox(models.Model):

    number = models.CharField('Number', max_length=30, help_text='What is this person\'s voice phone number?  This can include extentions.')
    primary = models.BooleanField('Is Primary', help_text='Is this the primary voice number?')
    restrict = models.BooleanField('Restrict Use', help_text='Should this number not be used for call lists and automated calls?')
    notes = models.CharField('Notes', max_length=255, blank=True, help_text='What are notes about this phone (ex "Ask for the floor manger", or "Don\'t call before noon")? ')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='For which person is this phone?')

    def __str__(self):
        return self.person + ': ' + self.number 

    class Meta:
        verbose_name_plural = "voxes"
        ordering = ['restrict', '-primary', 'number']

class RosterPlacement(models.Model):

    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, help_text='What is the roster of which the person is a member?')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Who is the person who is a member of this roster?')

    class Meta:
        ordering = ['roster', 'person']

    def __str__(self):
        if self.role_type > '':
            return self.event + ': ' + self.person + ': ' + self.role_type
        return self.event + ': ' + self.person 

class Residency(models.Model):

    district = models.ForeignKey(District, on_delete=models.CASCADE, help_text='What is the district in which the person lives?')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Who is the person who lives in this district?')

    def __str__(self):
        return self.district + ': ' + self.person

class Participation(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text='What is the event in which the person was a participant?')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Who is the person who participated in the event?')
    ROLE_TYPE_CHOICES=( 
        ('', 'Unknown or N/A'),
        ('aA', 'Attendee'),
        ('8C', 'Contributer'),
        ('6V', 'Volunteer'),
        ('4O', 'Organizing Assistant'),
        ('2L', 'Organizer/Leader'),
    )
    role_type = models.CharField('Role Type', max_length=2, blank=True,  help_text='What type of role did the person perform at or for the event?', choices=ROLE_TYPE_CHOICES)
    role_name = models.CharField('Role Name', max_length=40, blank=True, null=True, help_text='What is the name of the role that the person performed at the event? This can be left blank, in which case the role type will be used.')

    class Meta:
        ordering = ['event', 'role_type', 'person']

    def __str__(self):
        if self.role_type > '':
            return self.event + ': ' + self.person + ': ' + self.role_type
        return self.event + ': ' + self.person 

class SavedSearch(models.Model):

    user = models.ForeignKey(User, related_name="saved_search", on_delete=models.CASCADE, blank=True, null=True, help_text='To whom does this saved search belong?')
    searchstring = models.TextField('Filter String', blank=True, null=True, help_text='What is url encoded string for this search?') 
    name = models.CharField('Name', max_length=40, help_text='What is the name of this search?')
    is_public = models.BooleanField('Public', default=False, help_text='Should this search be available to all users?')
    hide_name = models.BooleanField('List With Name', default=True, help_text='If made public, should your name be shown on the list? (Admins may want to set False)')

class Params(models.Model):

    user = models.OneToOneField(User, related_name="params", on_delete=models.CASCADE, blank=True, null=True, help_text='Who is the user for this set of parameters?')
    last_searchstring = models.TextField('Filter String', blank=True, null=True, help_text='What is url encoded string for this search?') 

