# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: tagged.py 15 2008-08-15 15:36:47Z semente $
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
URL definitions for Tube videos divided by tag.
"""

from django.conf.urls.defaults import *
from tube.models import Video
from tube.settings import FLESHIN_NUM_LATEST

info_dict = {
    'paginate_by': FLESHIN_NUM_LATEST,
    'queryset_or_model': Video.published_on_site.all(),
    'template_name': 'tube/tube_list_tagged.html',
    'template_object_name': 'video',
}

tagged_video_list = url(        # videos by tag
    regex  = '^(?P<tag>[^/]+)/$',
    view   = 'tagged_object_list',
    kwargs = info_dict,
    name   = 'tube-tagged-video-list',
)

urlpatterns = patterns('tagging.views', tagged_video_list)
