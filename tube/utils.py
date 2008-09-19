# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: utils.py 2 2008-03-07 20:33:17Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007 Guilherme Mesquita Gondim
#
#  This file is part of django-tube.
#
#  django-tube is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


"""django-tube utilities."""

import tube

def get_svn_revision():
    """
    Returns the SVN revision in the form SVN-XXX, where XXX is the
    revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.
    """
    try:
        from django.utils import version
        rev = version.get_svn_revision(tube.__path__[0])
    except ImportError:
        rev = u'SVN-unknown'
    return rev
