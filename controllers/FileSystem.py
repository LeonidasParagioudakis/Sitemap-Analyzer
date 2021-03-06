#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FileSystem():

	def __init__(self,controller_object):
		self.controller_object = controller_object
		self.save_location_button = self.controller_object.builder.get_object("save_location_button")
		self.save_location_button.set_label('Save Location - ' + self.controller_object.save_file_path)
		self.main_window = self.controller_object.main_window
		self.save_location_button.connect('clicked',self.open_file_chooser_dialog)

	def open_file_chooser_dialog(self,widget):
		dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self.main_window, action=Gtk.FileChooserAction.OPEN)
		dialog.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK)
		self.add_filters_to_dialog(dialog)
		
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.controller_object.save_file_path = dialog.get_filename()
			self.save_location_button.set_label('Save Location - ' + self.controller_object.save_file_path)
		elif response == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()

	def add_filters_to_dialog(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)

		filter_py = Gtk.FileFilter()
		filter_py.set_name("Python files")
		filter_py.add_mime_type("text/x-python")
		dialog.add_filter(filter_py)
		
		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)
