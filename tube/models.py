# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: models.py 16 2008-08-15 19:42:46Z semente $
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

"""
Models definitions for Tube.
"""

import re
from datetime import datetime

from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from tube.managers import PublishedManager, CurrentSitePublishedManager
from tube.settings import HAS_TAG_SUPPORT

if HAS_TAG_SUPPORT:
    from tagging.fields import TagField

EMBED_VIDEO_OBJECT = """<object width="425" height="355">
    <param name="movie" value="http://www.youtube.com/v/%s&rel=0"></param>
    <param name="wmode" value="transparent"></param>
    <embed src="http://www.youtube.com/v/%s&rel=0"
           type="application/x-shockwave-flash" wmode="transparent"
           width="425" height="355"></embed>
</object>
"""

VIDEO_URL_PATTERN = re.compile(r'^http://www.youtube.com/watch\?v=([-a-z0-9A-Z_]+)')

class Category(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(
        _('slug'),
        help_text=_('Automatically built from the name. A slug is a short '
                    'label generally used in URLs.'),
    )
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name  = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('tube-video-category-list', None, {
            'category': str(self.slug),
        })

    def get_random_video(self):
        queryset = self.video_set.all()
        if queryset:
            return queryset.order_by('?')[0]
        return None

class Video(models.Model):
    title = models.CharField(_('title'), max_length=60)
    video_url = models.URLField(
        _('video URL'),
        help_text=_('Put the URL of the YouTube video. Example: '
                    'http://www.youtube.com/watch?v=wuzgCwKElm4')
    )
    slug = models.SlugField(
        _('slug'),
        help_text=_('Automatically built from the title. A slug is a short '
                    'label generally used in URLs.'),
    )
    date_recorded = models.DateField(_('date recorded'), blank=True, null=True)
    time_recorded = models.TimeField(_('time recorded'), blank=True, null=True)
    place = models.CharField(_('place'), blank=True, max_length=70)
    cameraman = models.CharField(
        _('cameraman'),
        blank=True,
        max_length=50
    )
    description = models.TextField(_('description'), blank=True)
    pub_date = models.DateTimeField(
        _('date published'),
        default=datetime.now,
        help_text=_('Videos in future dates are only published on '
                    'correct date.'),
    )
    is_published = models.BooleanField(_('published'), default=True)
    publish_on = models.ManyToManyField(
        Site,
        verbose_name=_('publish on'),
    )
    enable_comments = models.BooleanField(_('enable comments'), default=True)
    category = models.ForeignKey(Category, verbose_name=_('category'))

    if HAS_TAG_SUPPORT:
        tags = TagField(blank=True)

    # managers
    objects   = models.Manager()
    published = PublishedManager()
    on_site   = CurrentSiteManager('publish_on')
    published_on_site = CurrentSitePublishedManager('publish_on')

    class Meta:
        get_latest_by = 'pub_date'
        ordering      = ('-pub_date',)
        verbose_name  = _('video')
        verbose_name_plural = _('videos')

    def __unicode__(self):
        return self.title

    def get_video_id(self):
        match = re.match(VIDEO_URL_PATTERN, self.video_url)
        if match:
            return match.groups()[0]
        return None

    @permalink
    def get_absolute_url(self):
        return ('tube-video', None, {
            'category': str(self.category.slug),
            'slug' : str(self.slug),
        })

    def get_thumbnail_url(self):
        return 'http://i.ytimg.com/vi/%s/default.jpg' % self.get_video_id()

    def get_embed_video_object(self):
        video_id = self.get_video_id()
        return EMBED_VIDEO_OBJECT % (video_id, video_id)

    def in_future(self):
        return self.pub_date > datetime.now()

# signals
from django.db.models import signals

def video_pre_save(sender, instance, signal, *args, **kwargs):
    try:
        # update instance's pub_date if video was not published
        e = Video.objects.get(id=instance.id)
        if not e.is_published:
            instance.pub_date = datetime.now()
    except Video.DoesNotExist:
        pass

signals.pre_save.connect(video_pre_save, sender=Video)
