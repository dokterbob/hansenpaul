# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: views.py 11 2008-05-19 02:56:54Z semente $
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

from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from tube.models import Video, Category

def video_detail(request, category=None, *args, **kwargs):
    if category:
        kwargs['queryset'] = kwargs['queryset'].filter(category__slug__exact=category)
    return object_detail(request, *args, **kwargs)

def video_list(request, category=None, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.date_based.object_list``
    which creates a ``QuerySet`` containing only videos from ``category``
    argument, if specified.
    """
    if category:
        kwargs['queryset'] = kwargs['queryset'].filter(category__slug__exact=category)
        try:
            category_object = Category.objects.get(slug__exact=category)
            kwargs['extra_context']['category'] = category_object
        except KeyError:
            kwargs['extra_context'] = {'category': category_object}
    return object_list(request, *args, **kwargs)
