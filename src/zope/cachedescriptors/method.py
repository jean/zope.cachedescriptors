##############################################################################
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""Cached Methods

$Id$
"""

import BTrees.OOBTree


class cachedIn(object):
    """Cached method with given cache attribute."""

    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def __call__(self, func):

        def decorated(instance, *args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key = (args, tuple(kw))
            cache = self.cache(instance)
            try:
                v = cache[key]
            except KeyError:
                v = cache[key] = func(instance, *args, **kwargs)
            return v

        return decorated

    def cache(self, instance):
        try:
            cache = getattr(instance, self.attribute_name)
        except AttributeError:
            cache = BTrees.OOBTree.OOBTree()
            setattr(instance, self.attribute_name, cache)
        return cache
