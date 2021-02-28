#!/usr/bin/env python3
import os
import util.definitions
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from controllers.FileSystem import FileSystem
from controllers.TreeView import TreeView

class Controller():
    def __init__(self):
        self.builder = Gtk.Builder()
        tree_view_template_path = os.path.join(util.definitions.VIEWS_DIR,'tree_view.glade')
        self.builder.add_from_file(tree_view_template_path)
        self.main_window = self.builder.get_object("main_window")
        self.current_filter_language = None
        self.save_file_path = os.getcwd()
        self.init_controllers()

    def init_controllers(self):
        FileSystem(self)
        TreeView(self)
        

    def run(self):
        self.main_window.show_all()
        self.main_window.connect("destroy", Gtk.main_quit)
