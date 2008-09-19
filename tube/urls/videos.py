# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: videos.py 15 2008-08-15 15:36:47Z semente $
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
URL definitions for videos and categories.
"""

from django.conf.urls.defaults import *
from tube.models import Video, Category
from tube.settings import TUBE_NUM_LATEST

video_info_dict = {
    'queryset': Video.published_on_site.all(),
    'template_object_name': 'video',
}

video_detail = url(
    regex  = '^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$',
    view   = 'tube.views.video_detail',
    kwargs = dict(video_info_dict, slug_field='slug'),
    name   = 'tube-video'
)
video_list = url(               # all videos + category list
    regex  = '^$',
    view   = 'django.views.generic.list_detail.object_list',
    kwargs = dict(video_info_dict, paginate_by=TUBE_NUM_LATEST,
                  extra_context={'category_list': Category.objects.all}),
    name   = 'tube-video-list'
)
video_category_list = url(      # only videos in ``category``
    regex  = '^(?P<category>[-\w]+)/$',
    view   = 'tube.views.video_list',
    kwargs = dict(video_info_dict, paginate_by=TUBE_NUM_LATEST),
    name   = 'tube-video-category-list'
)

urlpatterns = patterns('', video_detail, video_list, video_category_list)
