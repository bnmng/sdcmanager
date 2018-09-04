from django.urls import path
from . import views

urlpatterns = [

    path('', views.PersonListView.as_view(), name='sdcpeople'),
    path('person/create/', views.PersonCreate.as_view(), name='person-create'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
    path('person/<int:pk>/update/', views.PersonUpdate.as_view(), name='person-update'),
    path('person/<int:pk>/delete/', views.PersonDelete.as_view(), name='person-delete'),

    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('group/create/', views.GroupCreate.as_view(), name='group-create'),
    path('group/<int:pk>', views.GroupDetailView.as_view(), name='group-detail'),
    path('group/<int:pk>/update/', views.GroupUpdate.as_view(), name='group-update'),
    path('group/<int:pk>/delete/', views.GroupDelete.as_view(), name='group-delete'),

    path('rosters/', views.RosterListView.as_view(), name='rosters'),
    path('roster/create/', views.RosterCreate.as_view(), name='roster-create'),
    path('roster/<int:pk>', views.RosterDetailView.as_view(), name='roster-detail'),
    path('roster/<int:pk>/update/', views.RosterUpdate.as_view(), name='roster-update'),
    path('roster/<int:pk>/delete/', views.RosterDelete.as_view(), name='roster-delete'),
]
