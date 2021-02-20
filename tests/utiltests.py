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
		random_header = Headers(browser='firefox',os='win',headers=True,)
		headers = util.request_helper.replace_browser_versions(random_header.generate())
		requests_data = {}
		requests_data['headers'] = headers
		requests_data['url'] = 'https://www.e-shop.gr/sitemap.xml'
		sitemap_items = util.struct.sitemap_reader('sitemap_products.phtml','loc',requests_data)
		self.assertFalse(sitemap_items is None)

if __name__ == '__main__':
	unittest.main()