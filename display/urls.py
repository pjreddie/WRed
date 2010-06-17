#Author: Joe Redmon
#urls.py

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from WRed.display.views import *
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from WRed.display.models import DataFile, MetaData

urlpatterns = patterns('',
    (r'^files/all$',all_files),
    (r'^files/all/$',all_files),
    (r'^files/(\w+)$', view_file),
    (r'^files/json/(\w+)/$', json_file_display),
    (r'^files/all/json/$', json_all_files),
    (r'^files/forms/upload/$', upload_file),
    (r'^files/forms/upload/live/$', upload_file_live),
    (r'^files/forms/delete/$', delete_file),
    (r'^files/pipeline/$', direct_to_template,{'template':'pipeline.html'}),
)
