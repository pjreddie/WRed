from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from fileviewer.display.views import json_all_files, json_file_display, upload_file, delete_file, view_file
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from fileviewer.display.models import DataFile, MetaData

urlpatterns = patterns('',
    (r'^files/(?P<md5>\w+)$', direct_to_template, {'template': 'view_file.html'}),
    (r'^files/all/$', direct_to_template, {'template':'all_files.html'}),
    (r'^chart/(?P<md5>\w+)/$', direct_to_template,{'template':'view_chart.html'}),
    (r'^files/json/(\w+)/$', json_file_display),
    (r'^files/all/json/$', json_all_files),
    (r'^files/forms/upload/$', upload_file),
    (r'^files/forms/delete/$', delete_file),
)
