from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from fileviewer.display.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from fileviewer.display.models import DataFile, MetaData

urlpatterns = patterns('',
    (r'^files/all/$', direct_to_template, {'template':'all_files.html'}),
    (r'^files/(?P<id>\w+)$', direct_to_template, {'template': 'view_file.html'}),
    (r'^chart/(?P<id>\w+)/$', direct_to_template,{'template':'view_chart.html'}),
    (r'^files/json/(\w+)/$', json_file_display),
    (r'^files/all/json/$', json_all_files),
    (r'^files/forms/upload/$', upload_file),
    (r'^files/forms/upload/live/$', upload_file_live),
    (r'^files/forms/delete/$', delete_file),
)
