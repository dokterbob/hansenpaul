# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: sitemaps.py 2 2008-03-07 20:33:17Z semente $
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

from django.contrib.sitemaps import Sitemap
from tube.models import Video

class TubeSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Video.published_on_site.all()

    def lastmod(self, obj):
        return obj.pub_date
