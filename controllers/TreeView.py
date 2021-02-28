#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import util.definitions
import util.struct

class TreeView():

	def __init__(self,controller_object):
		self.controller_object = controller_object
		self.item_text = self.controller_object.builder.get_object("item_text")
		self.recursion_text = self.controller_object.builder.get_object("recursion_text")
		self.sitemap_location_text = self.controller_object.builder.get_object("sitemap_location_text")
		self.start_button = self.controller_object.builder.get_object("start_button")
		
	def initiate_sitemap_reading(self):
		util.struct.sitemap_reader(self.item_text,)