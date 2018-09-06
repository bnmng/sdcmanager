# sdcpeople

## Introduction

SDCPeople is not yet finished

SDCpeople is a django app for listing people with information useful for a political organization.  Among other information, the app facilitates 
recording people's membership types, voting districts, and participation in groups and events.  SDCPeople was developed in Django 2.1.  I don't know how well it works
in other versions.

# Requirements

SDCPeople requires an existing Django project.  For those creating a new project for this app, I recommend naming the project something like "SDCManager".  I plan to 
write other apps which can be added to such a project.  

SDCPeople also requires the following to be implemented in the Django project.  Most of these are standard:

+ A functioning administration system with the ability to administer user permissions

# Installation

From the project directory (the directory with manage.py in it) clone the repository from github.org/bnmng/sdcpeople
'git clone https://github.com/bnmng/sdcpeople'

Add the SDC app to the projects settings file under INSTALLED_APPS

`sdcpeople.apps.SdcpeopleConfig`,

So the INSTALLED_APPS section of settings.py should be something like:

`
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sdcpeople.apps.SdcpeopleConfig',
]
`
Add the SDC urls to the projects's urls.py

`path('sdcpeople/', include('sdcpeople.urls')),`

So the urlpatterns section of urls.py should look something like

`
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='registration/profile.html'), name='user_profile'),
    path('admin/', admin.site.urls),
    path('sdcpeople/', include('sdcpeople.urls')),
    path('', RedirectView.as_view(url='/sdcpeople/'),name='home')
]
`


