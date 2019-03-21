from django.conf.urls import url
from .import views
from django.conf import settings 
from django.conf.urls.static import static
from django.shortcuts import render, redirect

urlpatterns=[
    url('^$',views.index, name = 'index'),
    url('^explore/',views.explore,name = 'explore'),
    url('^notifictaion/',views.notification,name = 'notification'),
    url('^profile/',views.profile,name = 'profile'),
    url('^login/',views.login,name = 'login'),
    url('^upload/',views.upload,name = 'upload'),
    url('^search/', views.search,name='search'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)