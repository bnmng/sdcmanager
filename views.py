from .forms import ApplicationForm, EmailForm, GroupForm, GroupMembershipForm, RosterForm, RosterPlacementForm, PersonForm, ResidencyForm, TxtmsgForm, VoxForm
from .models import Application, District, DistrictType, Email, Event, Roster, Group, GroupMembership, MembershipType, Params, Person, Residency, Txtmsg, SavedSearch, Vox
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
import copy
import datetime
import inspect
import logging


logger=logging.getLogger('django')

def get_inspect( info='' ):
    return ( '%s, %s, %s' % ( inspect.currentframe().f_back.f_code.co_name, inspect.currentframe().f_back.f_lineno, info ) )

class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 10

    def get(self, request):

        if 'delete_savedsearch' in self.request.GET and 'savedsearch' in self.request.GET and self.request.GET['savedsearch'] > '':
            try:
                savedsearch = SavedSearch.objects.get(id=self.request.GET['savedsearch'], user=self.request.user)
            except:
                pass
            else:
                savedsearch.delete()

        if 'use_savedsearch' in self.request.GET and 'savedsearch' in self.request.GET and self.request.GET['savedsearch'] > '':
            try:
                savedsearch = SavedSearch.objects.get(id=self.request.GET['savedsearch'])
            except:
                pass
            else:
                return redirect(reverse('sdcpeople') + '?' + savedsearch.searchstring)

        if self.request.META['QUERY_STRING'] == '':

            params = Params.objects.filter(user = self.request.user).last()
            if params is not None:
                searchstring = params.last_searchstring;
                if (searchstring > ""):
                    return redirect(reverse('sdcpeople') + '?' + searchstring)

            params = Params.objects.filter(user__isnull=True).last()
            if params is not None:
                searchstring = params.last_searchstring;
                if (searchstring > ""):
                    return redirect(reverse('sdcpeople') + '?' + searchstring)

        params, created = Params.objects.get_or_create(user_id=request.user.id)

        params.last_searchstring = self.request.META['QUERY_STRING'];
        params.save();

        if 'savesearch' in self.request.GET and 'savedsearch_name' in self.request.GET and self.request.GET['savedsearch_name'] > '':
            savedsearch, created = SavedSearch.objects.get_or_create(user_id=request.user.id, name=request.GET['savedsearch_name'])
            savedsearch.searchstring = self.request.META['QUERY_STRING'];
            savedsearch.save();
            
        return super().get(request)
        
    def get_queryset(self):
        queryset = super().get_queryset();

        if 'use_filterby_name' in self.request.GET and 'filterby_name' in self.request.GET:
            queryset = queryset.filter(
                Q(first_name__icontains=self.request.GET['filterby_name']) | Q(last_name__icontains=self.request.GET['filterby_name'])  
            )
        if 'use_filterby_membershiptype' in self.request.GET and 'filterby_membershiptype' in self.request.GET:
            queryset = queryset.filter(
                Q(membershiptype__id__in=self.request.GET.getlist('filterby_membershiptype'))
            )
        if 'use_filterby_group' in self.request.GET and 'filterby_group' in self.request.GET:
            queryset = queryset.filter(
                Q(group__id__in=self.request.GET.getlist('filterby_group'))
            )
        for districttype in DistrictType.objects.all():
            if 'use_filterby_districttypes[' + districttype.name + ']' in self.request.GET and 'filterby_districttypes[' + districttype.name + ']' in self.request.GET:
                queryset = queryset.filter(
                    Q(residency__district__id__in=self.request.GET.getlist('filterby_districttypes[' + districttype.name + ']'))
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        districttypelist=[]
        districttypes = DistrictType.objects.all()
        for districttype in districttypes:
            districttypelist.append({
                'name': districttype.name, 
                'use': self.request.GET.get('use_filterby_districttypes[' + districttype.name + ']'), 
                'district_choices': District.objects.filter(districttype_id = districttype.id),
                'values': self.request.GET.getlist('filterby_districttypes[' + districttype.name + ']')
            })
            
        context['districttypes'] = districttypelist

        context['membershiptype_choices'] = MembershipType.objects.all()

        context['group_choices'] = Group.objects.all()

        context['savedsearch_choices'] = SavedSearch.objects.filter(user_id=self.request.user.id)
    
        for getfield in ['filterby_membershiptype']:
            value = self.request.GET.getlist(getfield)
            if value:
                context[getfield] = value
                    
        for getfield in ['filterby_name']:
            value = self.request.GET.get(getfield)
            if value:
                context[getfield] = value

        for getfield in ['filterby_group']:
            value = self.request.GET.get(getfield)
            if value:
                context[getfield] = value

        for getfield in ['use_filterby_name', 'use_filterby_membershiptype', 'use_filterby_group' ]:
            value = self.request.GET.get(getfield)
            if value:
                context[getfield] = value

        context['quorum_all_count'] = Person.objects.filter(membershiptype__counts_quorum=True).count()

        return context

class PersonCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sdcpeople.add_person'
    model = Person
    form_class=PersonForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        districttype_all = DistrictType.objects.all()
        districttype_count = DistrictType.objects.count()

        districttype_names=[]
        for districttype in districttype_all:
            districttype_names.append( districttype.name )
        context['districttype_names'] = districttype_names

        ApplicationFormSet = inlineformset_factory(Person, Application, form=ApplicationForm, extra=1, fields='__all__')
        EmailFormSet = inlineformset_factory(Person, Email, form=EmailForm, extra=1, fields='__all__')
        GroupMembershipFormSet = inlineformset_factory(Person, GroupMembership, form=GroupMembershipForm, extra=1, fields='__all__')
        ResidencyFormSet = inlineformset_factory(Person, Residency, form=ResidencyForm, extra=districttype_count, fields='__all__')
        TxtmsgFormSet = inlineformset_factory(Person, Txtmsg, form=TxtmsgForm, extra=1, fields='__all__')
        VoxFormSet = inlineformset_factory(Person, Vox, form=VoxForm, extra=1, fields='__all__')

        if self.request.POST:

            applications = ApplicationFormSet(self.request.POST, instance = self.object)
            context['applications'] = applications

            emails = EmailFormSet(self.request.POST, instance = self.object)
            context['emails'] = emails

            groupmemberships = GroupMembershipFormSet(self.request.POST, instance = self.object)
            context['groupmemberships'] = groupmemberships

            residencies = ResidencyFormSet(self.request.POST, instance = self.object )

            for i in range( districttype_count):
                residencies.forms[i].fields['district'].queryset = District.objects.filter(districttype__id=districttype_all[i].id)
                residencies.forms[i].fields['district'].label =  districttype_all[i].name
            context['residencies'] = residencies

            txtmsgs = TxtmsgFormSet(self.request.POST, instance = self.object)
            context['txtmsgs'] = txtmsgs

            voxes = VoxFormSet(self.request.POST, instance = self.object)
            context['voxes'] = voxes

        else:

            applications = ApplicationFormSet( instance = self.object )
            context['applications'] = applications

            emails = EmailFormSet( instance = self.object )
            context['emails'] = emails

            groupmemberships = GroupMembershipFormSet( instance = self.object )
            context['groupmemberships'] = groupmemberships

            residencies = ResidencyFormSet( instance = self.object )
            for i in range( districttype_count):
                residencies.forms[i].fields['district'].queryset = District.objects.filter(districttype__id=districttype_all[i].id)
                residencies.forms[i].fields['district'].label =  districttype_all[i].name
            context['residencies'] = residencies

            txtmsgs = TxtmsgFormSet( instance = self.object )
            context['txtmsgs'] = txtmsgs

            voxes = VoxFormSet( instance = self.object )
            context['voxes'] = voxes

        return context

    def form_valid(self, form):
        form.instance._status = 1
        form.instance._created_by = self.request.user
        form.instance._created_date = datetime.datetime.now()
        form.instance._mod_by = self.request.user
        form.instance._mod_date = datetime.datetime.now()
    
        self.object = form.save()

        context = self.get_context_data()

        applications = context['applications']
        if applications.is_valid():
            applications.save()

        emails = context['emails']
        if emails.is_valid():
            emails.save()

        groupmemberships = context['groupmemberships']
        if groupmemberships.is_valid():
            groupmemberships.save()

        residencies = context['residencies']
        if residencies.is_valid():
            residencies.save()

        txtmsgs = context['txtmsgs']
        if txtmsgs.is_valid():
            txtmsgs.save()

        voxes = context['voxes']
        if voxes.is_valid():
            voxes.save()

        return super(PersonCreate, self).form_valid(form)

class PersonDetailView(LoginRequiredMixin, DetailView ):
    model = Person

class PersonUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sdcpeople.change_person'
    model = Person
    form_class=PersonForm 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        districttype_all = DistrictType.objects.all()
        districttype_count = DistrictType.objects.count()

        ApplicationFormSet = inlineformset_factory(Person, Application, form=ApplicationForm, extra=1, fields='__all__')
        EmailFormSet = inlineformset_factory(Person, Email, form=EmailForm, extra=1, fields='__all__')
        GroupMembershipFormSet = inlineformset_factory(Person, GroupMembership, form=GroupMembershipForm, extra=1, fields='__all__')
        ResidencyFormSet = inlineformset_factory(Person, Residency, form=ResidencyForm, extra=districttype_count, max_num=districttype_count, fields='__all__')
        TxtmsgFormSet = inlineformset_factory(Person, Txtmsg, form=TxtmsgForm, extra=1, fields='__all__')
        VoxFormSet = inlineformset_factory(Person, Vox, form=VoxForm, extra=1, fields='__all__')

        if self.request.POST:

            applications = ApplicationFormSet(self.request.POST, self.request.FILES, instance = self.object)
            context['applications'] = applications

            emails = EmailFormSet(self.request.POST, instance = self.object)
            context['emails'] = emails

            groupmemberships = GroupMembershipFormSet(self.request.POST, instance = self.object)
            context['groupmemberships'] = groupmemberships

            residencies = ResidencyFormSet(self.request.POST, instance = self.object)
            for i in range( districttype_count):
                residencies.forms[i].fields['district'].queryset = District.objects.filter(districttype__id=districttype_all[i].id)
                residencies.forms[i].fields['district'].label =  districttype_all[i].name
            context['residencies'] = residencies

            txtmsgs = TxtmsgFormSet(self.request.POST, instance = self.object)
            context['txtmsgs'] = txtmsgs

            voxes = VoxFormSet(self.request.POST, instance = self.object)
            context['voxes'] = voxes

        else:

            applications = ApplicationFormSet( instance = self.object )
            context['applications'] = applications

            emails = EmailFormSet( instance = self.object )
            context['emails'] = emails

            groupmemberships = GroupMembershipFormSet( instance = self.object )
            context['groupmemberships'] = groupmemberships

            residencies = ResidencyFormSet( instance = self.object )
            for i in range( districttype_count):
                residencies.forms[i].fields['district'].queryset = District.objects.filter(districttype__id=districttype_all[i].id)
                residencies.forms[i].fields['district'].label =  districttype_all[i].name
            context['residencies'] = residencies

            txtmsgs = TxtmsgFormSet( instance = self.object )
            context['txtmsgs'] = txtmsgs

            voxes = VoxFormSet( instance = self.object )
            context['voxes'] = voxes


        return context

    def form_valid(self, form):

        form.instance_mod_by = self.request.user
        form.instance._mod_date = datetime.datetime.now()

        self.object = form.save()

        context = self.get_context_data()

        applications = context['applications']
        if applications.is_valid():
            applications.save()

        txtmsgs = context['txtmsgs']
        if txtmsgs.is_valid():
            txtmsgs.save()

        emails = context['emails']
        if emails.is_valid():
            emails.save()

        groupmemberships = context['groupmemberships']
        if groupmemberships.is_valid():
            groupmemberships.save()


        residencies = context['residencies']
        if residencies.is_valid():
            residencies.save()

        voxes = context['voxes']
        if voxes.is_valid():
            voxes.save()

        return super().form_valid(form)

class PersonDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sdcpeople.delete_person'
    model = Person
    success_url = reverse_lazy('sdcpeople')


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 10

class GroupCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sdcpeople.add_group'
    model = Group
    form_class=GroupForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        GroupMembershipFormSet = inlineformset_factory(Group, GroupMembership, form=GroupMembershipForm, extra=1, fields='__all__')

        groupmemberships = GroupMembershipFormSet( instance = self.object )
        context['groupmemberships'] = groupmemberships

        return context

    def form_valid(self, form):

        self.object = form.save()

        context = self.get_context_data()

        groupmemberships = context['groupmemberships']
        if groupmemberships.is_valid():
            groupmemberships.save()

        return super(GroupCreate, self).form_valid(form)

class GroupDetailView(LoginRequiredMixin, DetailView ):
    model = Group

class GroupUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sdcpeople.change_group'
    model = Group
    form_class=GroupForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        GroupMembershipFormSet = inlineformset_factory(Group, GroupMembership, form=GroupMembershipForm, extra=1, fields='__all__')
        
        if self.request.POST:

            groupmemberships = GroupMembershipFormSet(self.request.POST, instance = self.object )
            context['groupmemberships'] = groupmemberships

        else:

            groupmemberships = GroupMembershipFormSet( instance = self.object )
            groupmemberships.refresh_total_form_count = groupmemberships.total_form_count()
            context['groupmemberships'] = groupmemberships

        return context

    def form_valid(self, form):

        self.object = form.save()

        context = self.get_context_data()

        groupmemberships = context['groupmemberships']
        if groupmemberships.is_valid():
            groupmemberships.save()

        return super().form_valid(form)

class GroupDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sdcpeople.delete_group'
    model = Group
    success_url = reverse_lazy('groups')

class RosterListView(LoginRequiredMixin, ListView):
    model = Roster
    paginate_by = 10

class RosterCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sdcpeople.add_roster'
    model = Roster
    form_class=RosterForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        RosterPlacementFormSet = inlineformset_factory(Roster, RosterPlacement, form=RosterPlacementForm, extra=1, fields='__all__')

        rosterplacements = RosterPlacementFormSet( instance = self.object )
        context['rosterplacements'] = rosterplacements

        return context

    def form_valid(self, form):

        self.object = form.save()

        context = self.get_context_data()

        rosterplacements = context['rosterplacements']
        if rosterplacements.is_valid():
            rosterplacements.save()

        return super(RosterCreate, self).form_valid(form)

class RosterDetailView(LoginRequiredMixin, DetailView ):
    model = Roster

class RosterUpdate(LoginRequiredMixin, UpdateView):
    permission_required = 'sdcpeople.change_roster'
    model = Roster
    form_class=RosterForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        RosterPlacementFormSet = inlineformset_factory(Roster, RosterPlacement, form=RosterPlacementForm, extra=1, fields='__all__')
        
        if self.request.POST:

            rosterplacements = RosterPlacementFormSet(self.request.POST, instance = self.object )
            context['rosterplacements'] = rosterplacements

        else:

            rosterplacements = RosterPlacementFormSet( instance = self.object )
            rosterplacements.refresh_total_form_count = rosterplacements.total_form_count()
            context['rosterplacements'] = rosterplacements

        return context

    def form_valid(self, form):

        self.object = form.save()

        context = self.get_context_data()

        rosterplacements = context['rosterplacements']
        if rosterplacements.is_valid():
            rosterplacements.save()

        return super().form_valid(form)

class RosterDelete(LoginRequiredMixin, DeleteView):
    permission_required = 'sdcpeople.delete_roster'
    model = Roster
    success_url = reverse_lazy('rosters')
