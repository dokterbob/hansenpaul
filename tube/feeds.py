# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: feeds.py 2 2008-03-07 20:33:17Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2008 Guilherme Mesquita Gondim
#
#  This file is part of django-tube.
#
#  django-tube is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#

from django.conf import settings
from django.contrib.comments.models import FreeComment
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from tube.models import Video, Category
from tube.settings import HAS_TAG_SUPPORT

if HAS_TAG_SUPPORT:
    from tagging.models import Tag

class RssVideosFeed(Feed):
    """
    All videos RSS feed.
    """
    description = _('Latest videos on site')
    title_template = 'feeds/tube_video_title.html'
    description_template = 'feeds/tube_video_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's videos") % {'title': self._site.name}

    def link(self):
        return reverse('tube-video-list')

    def get_query_set(self):
        return Video.published_on_site.order_by('-pub_date')

    def items(self):
        return self.get_query_set()[:15]

    def item_pubdate(self, item):
        return item.pub_date

    def item_categories(self, item):
        try:
            return item.tags.split()
        except AttributeError:
            pass      # ignore if not have django-tagging support

class AtomVideosFeed(RssVideosFeed):
    """
    All videos Atom feed.
    """
    feed_type = Atom1Feed
    subtitle = RssVideosFeed.description



class RssCategoriesFeed(Feed):
    """
    All video categories RSS feed.
    """
    description = _('Latest video categories on site')
    title_template = 'feeds/tube_category_title.html'
    description_template = 'feeds/tube_category_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's video categories") % {'title': self._site.name}

    def link(self):
        return reverse('tube-video-list')

    def get_query_set(self):
        return Category.objects.all()

    def items(self):
        return self.get_query_set()[:15]

class AtomCategoriesFeed(RssCategoriesFeed):
    """
    All video categories Atom feed.
    """
    feed_type = Atom1Feed
    subtitle = RssCategoriesFeed.description



class RssVideosByTagFeed(RssVideosFeed):
    """
    RSS feeds for videos divided by tags.
    """
    def get_object(self, bits):
        # In case of "rss/tag/example/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=bits[0])

    def title(self, obj):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _('%(title)s: videos tagged "%(tag name)s"') % \
               {'title': self._site.name, 'tag name': obj.name}

    def description(self, obj):
        return _('Latest videos for tag "%(tag name)s"') % \
               {'tag name': obj.name}

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('tube-tagged-video-list', args=[obj.name])

    def get_query_set(self):
        queryset = Video.published_on_site.filter(tags__contains=obj.name)
        return queryset.order_by('-pub_date')

    def items(self, obj):
        return self.get_query_set()[:15]

class AtomVideosByTagFeed(RssVideosByTagFeed):
    """
    Atom feeds for videos divided by tags.
    """
    feed_type = Atom1Feed
    subtitle = RssVideosByTagFeed.description



class RssVideosByCategoryFeed(RssVideosFeed):
    """
    RSS feeds for videos divided by categories.
    """
    def get_object(self, bits):
        # In case of "rss/category/example/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(name__exact=bits[0])

    def title(self, obj):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _('%(title)s: videos of category "%(category name)s"') % \
               {'title': self._site.name, 'category name': obj.name}

    def description(self, obj):
        return _('Latest videos for category "%(category name)s"') % \
               {'category name': obj.name}

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('tube-video-category-list', args=[obj.name])

    def get_query_set(self):
        queryset = Video.published_on_site.filter(category__exact=obj.name)
        return queryset.order_by('-pub_date')

    def items(self, obj):
        return self.get_query_set()[:15]

class AtomVideosByCategoryFeed(RssVideosByCategoryFeed):
    """
    Atom feeds for videos divided by categories.
    """
    feed_type = Atom1Feed
    subtitle = RssVideosByCategoryFeed.description



class RssFreeCommentsFeed(Feed):
    description = _('Latest comments on videos')
    title_template = 'feeds/comments_title.html'
    description_template = 'feeds/comments_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's video comments") % \
               {'title': self._site.name}

    def link(self):
        return reverse('tube-category-list')

    def item_pubdate(self, item):
        return item.submit_date

    def get_query_set(self):
        get_list_function = FreeComment.objects.filter
        kwargs = {
            'is_public': True,
            'site__pk': settings.SITE_ID,
            'content_type__app_label__exact': 'tube',
            'content_type__model__exact': 'video',
        }
        return get_list_function(**kwargs)

    def items(self):
        return self.get_query_set()[:30]

class AtomFreeCommentsFeed(RssFreeCommentsFeed):
    feed_type = Atom1Feed
    subtitle = RssFreeCommentsFeed.description
