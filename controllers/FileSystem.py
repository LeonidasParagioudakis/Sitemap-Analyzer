#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os

class FileSystem():

	def __init__(self,controller_object):
		self.controller_object = controller_object
		self.save_location_button = self.controller_object.builder.get_object("save_location_button")
		self.main_window = self.controller_object.main_window
		self.save_location_button.connect('clicked',self.open_file_chooser_dialog)

	def open_file_chooser_dialog(self,widget):
		dialog = Gtk.FileChooserDialog(title="Please choose a file - or type to create one", 
										parent=self.main_window, 
										action=Gtk.FileChooserAction.SAVE)
		dialog.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK)
		self.add_filters_to_dialog(dialog)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			selection = dialog.get_filename()
			file_selected_or_created = self.handle_file_selection(selection)
			if file_selected_or_created:
				self.controller_object.save_file_path = selection
		elif response == Gtk.ResponseType.CANCEL:
			pass
		
		dialog.destroy()

	def handle_file_selection(self,selection):
		if os.path.isfile(selection):
			try:
				response = self.warning_dialog("File in" + str(selection) + " is not empty. Do you want to proceed?")
				if response == Gtk.ResponseType.OK:
					return selection
			except Exception as e:
				print(e)
		elif not os.path.isfile(selection):
			try:
				with open(selection, 'a') as f:
					os.utime(selection)
				return selection
			except OSError as e:
				self.warning_dialog("You do not have permission to create file in" + str(selection))
		return False

	def warning_dialog(self,message):
		dialog = Gtk.MessageDialog(
			transient_for=self.main_window,
			flags=0,
			message_type=Gtk.MessageType.WARNING,
			text=message,
		)
		dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
		response = dialog.run()
		dialog.destroy()
		return response

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
