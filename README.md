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
+ A login page
+ A url entry named 'home'.  This is described in the installation section.

# Installation

## Get the files

From the project root directory (the directory with manage.py in it) clone the repository from github.org/bnmng/sdcpeople
`git clone https://github.com/bnmng/sdcpeople`

## Update settings.py

Add the SDC app to the project's settings file under INSTALLED_APPS

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

## Update urls.py

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

Also in urls.py, make sure the following import line is present
` from django.conf.urls import include`

SDCPeople requires a url named 'home', because there is an item labeled 'Home' in the menubar.  The url of that item can be whatever you want.  If you want  the home 
item to point the home screen of the SDCPeople app, then, in your project's urls.py,  import RedirectView from django.views.generic
`from django.views.generic import RedirectView`
and add the following to your urlpatterns:
`path('', RedirectView.as_view(url='/sdcpeople/'),name='home')`

## Perform the migrations

From the project root directory run
`python manage.py migrate`

Hopefull that went smoothly.  

## Add permissions for users

In order to use SDCpeople, your users need appropriate permissions.  The migrations created a user group named "sdcpeople_editors".  
Users in this group have access to all functions defined in the SDCPeople application.  

Some models can only be edited through the admin panel.  


