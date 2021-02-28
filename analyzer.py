#!/usr/bin/env python3
import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import util.definitions
from controllers.Controller import Controller


app = Controller()
app.run()
Gtk.main()
