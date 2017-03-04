# coding: utf-8

__author__ = 'Ryo HIGASHIGAWA'
__version__ = '0.0.1'
__licencse__ = 'MIT'


class Routing(object):
    """URL mapping class."""

    _routing = []

    @classmethod
    def add(cls, routings):
        """add a routing."""
        cls._routing.extend(routings)

    @classmethod
    def config(cls):
        """output routing to standard I/O."""
        print(cls._routing)
