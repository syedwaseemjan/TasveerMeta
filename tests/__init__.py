# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~
    tests package
"""
import sys
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.abspath(os.path.join(PROJECT_DIR, "app")))

import config as test_config
from unittest import TestCase
from app import config

for attribute in dir(config):
    if not attribute.startswith("__"):
        setattr(config, attribute, getattr(test_config, attribute))


class TasveerMetaAppTestCase(TestCase):
    """TasveerMetaAppTestCase is not doing anything special
    but we can place any common functionality in it in future
    if we want to add more tests.
    """

    def setUp(self):
        super(TasveerMetaAppTestCase, self).setUp()

    def tearDown(self):
        super(TasveerMetaAppTestCase, self).tearDown()
