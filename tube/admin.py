# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: admin.py 14 2008-07-31 12:02:50Z semente $
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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tube.models import Category, Video
from tube.settings import HAS_TAG_SUPPORT

from django.contrib.sites.models import Site


if HAS_TAG_SUPPORT:
    TAG_FIELD = ['tags']
else:
    TAG_FIELD = []


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'video_url', 'slug', 'category')
        }),
        (_('Video detail'), {
            'classes': ('collapse',),
            'fields': ['date_recorded', 'time_recorded', 'place',
                       'description', 'cameraman'] + TAG_FIELD
        }),
        (_('Status'), {
            'classes': ('collapse',),
            'fields': ('is_published', 'publish_on')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('pub_date',),
        })
    )
    list_display = ('thumbnail', 'title', 'date_recorded', 'time_recorded', 'pub_date',
                    'place', 'category', 'is_published', 'enable_comments')
    list_filter = ('is_published', 'publish_on', 'enable_comments', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['slug', 'place', 'title', 'description', 'cameraman']
    
    def thumbnail(self, myvideo):
       return u'<img src="%s" alt="%s"/>' % (myvideo.get_thumbnail_url(), myvideo)
    thumbnail.short_description = _('thumbnail')
    thumbnail.allow_tags = True
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'publish_on': # Check if it's the one you want
            kwargs.update({'initial': [Site.objects.get_current()]})
         
        return super(VideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)
