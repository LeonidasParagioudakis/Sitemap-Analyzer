#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import util.definitions
import util.struct
import re

class TreeView():

	def __init__(self,controller_object):
		self.controller_object = controller_object
		self.main_window = self.controller_object.main_window
		self.item_text = self.controller_object.builder.get_object("item_text")
		self.recursion_text = self.controller_object.builder.get_object("recursion_text")
		self.sitemap_location_text = self.controller_object.builder.get_object("sitemap_location_text")
		self.start_button = self.controller_object.builder.get_object("start_button")
		self.start_button.connect('clicked',self.initiate_sitemap_reading)

	def warning_dialog_on_empty_entry(self,message):
		dialog = Gtk.MessageDialog(
			transient_for=self.main_window,
			flags=0,
			message_type=Gtk.MessageType.WARNING,
			buttons=Gtk.ButtonsType.OK,
			text=message,
		)
		dialog.run()
		dialog.destroy()

	def input_is_valid(self):
		self.recursion_text_value = self.recursion_text.get_text()
		self.item_text_value = self.item_text.get_text()
		self.sitemap_location_text_value = self.sitemap_location_text.get_text()
		if (not self.text_value_is_valid()) or (not self.recursion_text_is_valid()) or (not self.sitemap_location_text_is_valid()):
			return False
		return True

	def text_value_is_valid(self):
		if not self.item_text_value:
			self.warning_dialog_on_empty_entry(self.item_text.get_name()+" cannot be empty")
			return False
		return True
	
	def recursion_text_is_valid(self):
		if not self.recursion_text_value:
			self.warning_dialog_on_empty_entry(self.recursion_text.get_name()+" cannot be empty")
			return False
		return True
	
	def sitemap_location_text_is_valid(self):
		if not self.sitemap_location_text_value:
			self.warning_dialog_on_empty_entry(self.sitemap_location_text.get_name()+" cannot be empty")
			return False
		elif re.search(r"^http.*?", self.sitemap_location_text_value) is None:
			self.warning_dialog_on_empty_entry(self.sitemap_location_text.get_name()+" should be a valid sitemap url ")
			return False
		return True

	def initiate_sitemap_reading(self,widget):
		if self.input_is_valid():
			util.struct.sitemap_reader(self.recursion_text_value,self.item_text_value,self.sitemap_location_text_value,self.controller_object.save_file_path)
