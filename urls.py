from django.conf.urls.defaults import *

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from tube.feeds import *

feeds = {
    'rss': RssVideosFeed,
    'atom' : AtomVideosFeed
}

from tube.sitemaps import *
sitemaps = {
    'tube' : TubeSitemap
}

urlpatterns = patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT + '/static/' }),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/(.*)', admin.site.root),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^guestbook/', include('guestbook.urls')),    
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^', include('tube.urls.videos')),
)
