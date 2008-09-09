from django.conf.urls.defaults import *

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from tube.feeds import *

feeds = {
    'rss': RssVideosFeed,
    'atom' : AtomVideosFeed
}

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT + '/static/' }),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/(.*)', admin.site.root),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^', include('tube.urls.videos')),
)
