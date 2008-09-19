# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: managers.py 2 2008-03-07 20:33:17Z semente $
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
Custom managers for Django models registered with Tube application.
"""

from datetime import datetime
from django.contrib.sites.managers import CurrentSiteManager
from django.db.models import Manager
from tube.settings import HAS_TAG_SUPPORT


class PublishedManager(Manager):
    """
    Manager for published videos on all sites. A published video have the
    field ``is_published`` as ``True`` and/or ``pub_date`` in non-future
    date.
    """

    def get_query_set(self):
        queryset = super(PublishedManager, self).get_query_set()
        return queryset.filter(is_published=True, pub_date__lte=datetime.now)

    if HAS_TAG_SUPPORT:
        def tagged(self, tag_instance):
            """
            Returns a QuerySet for a tag.
            """
            from tagging.models import TaggedItem
            return TaggedItem.objects.get_by_model(self.get_query_set(),
                                                   tag_instance)

class CurrentSitePublishedManager(CurrentSiteManager):
    """
    Manager for published videos on current site. A published video have the
    field ``is_published`` as ``True`` and/or ``pub_date`` in non-future
    date.
    """

    def get_query_set(self):
        queryset = super(CurrentSitePublishedManager, self).get_query_set()
        return queryset.filter(is_published=True, pub_date__lte=datetime.now)

    if HAS_TAG_SUPPORT:
        def tagged(self, tag_instance):
            """
            Returns a QuerySet for a tag.
            """
            from tagging.models import TaggedItem
            return TaggedItem.objects.get_by_model(self.get_query_set(),
                                                   tag_instance)
