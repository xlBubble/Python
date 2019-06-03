"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from data.views import login, manage, check_start,show_region


urlpatterns = [
    url(r'^data/', include('data.urls')),
    url(r'^$', login.homepage),
    url(r'^index', login.homepage),
    url(r'^login', login.login),
    url(r'^register', login.ajax_register),
    url(r'^403', manage.manage),
    url(r'^logout', manage.logout),
    url(r'^manage', manage.manage),
    url(r'^show_region', show_region.show_region),
    url(r'^cli_add', manage.cli_add),
    url(r'^api_confirm', manage.api_confirm),
    url(r'^show_cli$', manage.show_cli),
    url(r'^show_cli_name$', manage.show_cli_name),
    url(r'^show_cli_account$', manage.show_cli_account),
    url(r'^show_event_info$', manage.show_event_info),
    url(r'^add_event', manage.add_event),
    url(r'^check_start', check_start.check_start),
]
