"""djmemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from app1 import views as app1_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='admin_site'),
    
    # user urls
    url(r'^$', app1_views.get_list, name='memo_get_list'),
    url(r'^detail/(\d+)/$', app1_views.get_detail, name='memo_get_detail'),
    url(r'^new_memo/$', app1_views.new_memo, name='memo_new_memo'),
    url(r'^new_section/(\d+)/$', app1_views.add_section, name='memo_new_section'),
    url(r'^new_chapter/(\d+)/$', app1_views.add_chapter, name='memo_new_chapter'),
    url(r'^edit_section/(\d+)/(\d+)/$', app1_views.edit_section, name='memo_edit_section'),
    url(r'^edit_summary/(\d+)/$', app1_views.edit_summary, name='memo_edit_summary'),
    url(r'^update_task/(\d+)/$', app1_views.update_task, name='memo_update_task'),
    url(r'^export_task/$', app1_views.export_task, name='memo_export_task'),

]
