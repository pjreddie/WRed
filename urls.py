#Author: Joe Redmon
#urls.py

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from WRed.display.views import *
from django.http import HttpResponse
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
static_files_dict = {
    'document_root': os.path.join(SITE_ROOT, 'media/'),
}

urlpatterns = patterns('',
    # (r'^$', direct_to_template, {'template':'index.html'}),
    (r'^WRed/', include('WRed.display.urls')),
    # Example:
    # (r'^WRed/', include('WRed.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /*", mimetype="text/plain")),
    # Remove below when moving to production server
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', static_files_dict),
    (r'^accounts/login/$', login_view),
    (r'^accounts/logout/$', logout_view),
)
