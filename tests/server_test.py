# -*- coding: utf-8 -*-

from . import TasveerMetaAppTestCase
from app.main import Main


class ServerTestCase(TasveerMetaAppTestCase):
    """
    ServerTestCase constains all unit tests for StatsCollector App.
    """

    def setUp(self):
        super(ServerTestCase, self).setUp()
        Main()
