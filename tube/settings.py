# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: settings.py 2 2008-03-07 20:33:17Z semente $
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
Default Tube application settings.

If you not configure the settings below in your own project settings.py,
they assume default values::

    TUBE_NUM_LATEST
        Number of latest itens on object_list view. Default: 10.
"""

from django.conf import settings


#
#  (!!!)
#
#  DON'T EDIT THESE VALUES, CONFIGURE IN YOUR OWN PROJECT settings.py
#

TUBE_NUM_LATEST = getattr(settings, 'TUBE_NUM_LATEST', 10)


# django-tagging support
HAS_TAG_SUPPORT = 'tagging' in settings.INSTALLED_APPS
try:
    import tagging
except ImportError:
    HAS_TAG_SUPPORT = False
