#!/usr/bin/env python3
import unittest
import sys
from os.path import dirname, abspath,join
sys.path.insert(1, dirname(dirname(abspath(__file__))))
import util.request_helper
import util.struct
import requests
import json
from fake_headers import Headers

class TestUtil(unittest.TestCase):

	def test_recursive_read(self):
		sitemap_items = util.struct.sitemap_reader('sitemap_products.phtml','loc','https://www.e-shop.gr/sitemap.xml')
		self.assertFalse(sitemap_items is None)

if __name__ == '__main__':
	unittest.main()