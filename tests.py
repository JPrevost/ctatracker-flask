# -*- coding: utf-8 -*-
from __future__ import absolute_import
import app.bustimes
import unittest

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app.bustimes.app.config['TESTING'] = True
        self.app = app.bustimes.app.test_client()

    def test_routes_page(self):
        r = self.app.get('/')
        assert b'Choose a Route' in r.data
        assert b'147 Outer Drive Express' in r.data

    def test_directions_page(self):
        r = self.app.get('/directions/147/Outer%20Drive%20Express')
        assert b'Choose a Direction' in r.data
        assert b'Northbound' in r.data
        assert b'Southbound' in r.data

    def test_stops_page(self):
        r = self.app.get('/stops/147/Outer%20Drive%20Express/Northbound')
        assert b'Choose a Stop' in r.data
        assert b'Michigan &amp; Huron' in r.data
        assert b'Sheridan &amp; Foster' in r.data

    def test_predictions_page(self):
        r = self.app.get('/predictions/147/Outer%20Drive%20Express/Northbound/1125')
        assert b'Predictions' in r.data
        assert b'Michigan &amp; Huron' in r.data

if __name__ == '__main__':
    unittest.main()
