#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import util.definitions
import util.struct
import re
import requests
import util.request_helper
from fake_headers import Headers
import time
import threading

class TreeView():

	def __init__(self,controller_object):
		self.controller_object = controller_object
		self.main_window = self.controller_object.main_window
		self.item_text = self.controller_object.builder.get_object("item_text")
		self.recursion_text = self.controller_object.builder.get_object("recursion_text")
		self.sitemap_location_text = self.controller_object.builder.get_object("sitemap_location_text")
		self.start_button = self.controller_object.builder.get_object("start_button")
		self.initialize_list_store()
		self.start_button.connect('clicked',self.initiate_sitemap_reading)

	def initialize_list_store(self):
		self.sitemap_objects_liststore = Gtk.ListStore(str)
		self.tree_view = self.controller_object.builder.get_object("main_window_tree_view")
		self.tree_view.set_model(self.sitemap_objects_liststore)
		cellRenderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Title", cellRenderer, text=0)
		self.tree_view.append_column(column)

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

	def append_to_file(self,file_store_location,item):
		with open(file_store_location,'a') as sitemap_file:
			sitemap_file.write(item + '\n')

	def sitemap_reader(self,sitemap_indicator,element,sitemap_url,file_store_location):
		try:
			requests_data = {}        
			random_header = Headers(browser='firefox',os='win',headers=True,)
			headers = util.request_helper.replace_browser_versions(random_header.generate())
			requests_data['headers'] = headers
			requests_data['url'] = sitemap_url
			sitemap_str = requests.get(**requests_data)

			for item in re.finditer(r"<"+str(element)+">(.*?)<\/"+str(element)+">", sitemap_str.text, re.MULTILINE):
				if sitemap_indicator in item.group(1):
					print ('Going deeper to ',item.group(1))
					self.sitemap_reader(sitemap_indicator,element,item.group(1),file_store_location)
				elif (item.group(1) is not None):
					self.sitemap_objects_liststore.append([str(item.group(1))])
					self.append_to_file(file_store_location,item.group(1))

		except Exception as e:
			print(e)

	def initiate_sitemap_reading(self,widget):
		if self.input_is_valid():
			self.sitemap_reading_thread = threading.Thread(target=self.sitemap_reader,args=(
				self.recursion_text_value,self.item_text_value,self.sitemap_location_text_value,self.controller_object.save_file_path))
			self.sitemap_reading_thread.daemon = True
			self.sitemap_reading_thread.start()
