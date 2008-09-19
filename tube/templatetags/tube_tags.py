# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: tube_tags.py 9 2008-05-19 02:49:37Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007, 2008 Guilherme Mesquita Gondim
#
#  This file is part of django-tube.
#
#  django-tube is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


"""
The ``tube.templatetags.tube_tags`` module defines a number of
template tags which may be used to work with videos and your
comments.

To access django-tube template tags in a template, use the {% load %}
tag::

    {% load tube_tags %}
"""

from django import template
from django.conf import settings
from django.contrib.comments.models import FreeComment
from tube.models import Video


register = template.Library()

class VideoListNode(template.Node):
    def __init__(self, num, var_name, category=None):
        try:
            if category == None:
                self.category = None
            else:
                self.category = int(category)
        except ValueError:
            self.category =  template.Variable(category)
        self.num = int(num)
        self.var_name = var_name

    def render(self, context):
        if self.category != None and type(self.category) != int:
            try:
                self.category = self.category.resolve(context)
                if self.category == None:
                    return ''
            except template.VariableDoesNotExist:
                return ''
        video_list = Video.published_on_site.all()
        if self.category != None:
            video_list = video_list.filter(category=self.category)
        context[self.var_name] = list(video_list[:self.num])
        return ''

def do_get_tube_video_list(parser, token):
    """
    Gets videos list and populates the template context with a variable
    containing that value, whose name is defined by the 'as' clause.

    Syntax::

        {% get_tube_video_list [num] (from [category]) as [var_name] %}

    Example usage to get latest videos::

        {% get_tube_video_list 10 as latest_videos %}

    To get videos from category with id `1`::

        {% get_tube_video_list 10 from 1 as video_list %}

    To get videos from category with a context variable do::

        {% get_tube_video_list 10 from video.category as videos_from_even_category %}

    Note: The start point is omitted.
    """
    bits = token.contents.split()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
        return VideoListNode(num=bits[1], var_name=bits[3])
    if len(bits) == 6:
        if bits[2] != 'from':
            raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'from'" % bits[0]
        if bits[4] != 'as':
            raise template.TemplateSyntaxError, "Fourth argument to '%s' tag must be 'as'" % bits[0]
        return VideoListNode(num=bits[1], var_name=bits[5], category=bits[3])
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes three or five arguments" % bits[0]


class CommentListNode(template.Node):
    def __init__(self, num, var_name, start=0, free=True):
        try:
            self.start = int(start)
        except ValueError:
            self.start =  template.Variable(start)
        self.num = int(num)
        self.var_name = var_name
        self.free = free

    def render(self, context):
        if type(self.start) != int:
            try:
                self.start =  int(self.start.resolve(context))
            except template.VariableDoesNotExist:
                return ''
        get_list_function = self.free and FreeComment.objects.filter
        kwargs = {
            'is_public': True,
            'site__pk': settings.SITE_ID,
            'content_type__app_label__exact': 'tube',
            'content_type__model__exact': 'video',
        }
        comment_list = get_list_function(**kwargs).select_related()
        context[self.var_name] = comment_list[self.start:][:self.num]
        return ''

def do_get_tube_free_comment_list(parser, token):
    """
    Gets Tube's FreeComment list and populates the template context with a
    variable containing that value, whose name is defined by the 'as' clause.

    Syntax::

        {% get_tube_free_comment_list [num] (from the [start]) as [var_name] %}

    Example usage to get latest comments::

        {% get_tube_free_comment_list 10 as latest_tube_comments %}

    To get old comments::

        {% get_tube_free_comment_list 10 from the 10 as old_comments %}

    To get previous comments from the last comment on page with
    ``last_on_page`` context variable provided by ``object_list``, do::

        {% get_tube_free_comment_list 10 from the last_on_page as old_comments %}

    Note: The start point is omitted.
    """
    bits = token.contents.split()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
        return CommentListNode(bits[1], bits[3], free=True)
    if len(bits) == 7:
        if bits[2] != 'from' or bits[3] != 'the':
            raise template.TemplateSyntaxError, "Third and fourth arguments to '%s' tag must be 'from the'" % bits[0]
        if bits[5] != 'as':
            raise template.TemplateSyntaxError, "Fifth argument to '%s' tag must be 'as'" % bits[0]
        return CommentListNode(bits[1], bits[6], bits[4], free=True)
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes four or seven arguments" % bits[0]


register.tag('get_tube_video_list', do_get_tube_video_list)
register.tag('get_tube_free_comment_list', do_get_tube_free_comment_list)
