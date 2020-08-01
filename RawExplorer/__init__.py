import os
import tkinter as tk
import tkinter.filedialog

from kivy.app import App
from kivy.base import EventLoop
import kivy.properties as kpt
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from RawExplorer.scripts import import_scripts
from RawExplorer.tabs.CreatureView import CreatureView
# from .tabs.ItemView import ItemView
from RawExplorer.widgets.DropDown import DropDown
from RawExplorer.raws import RawCollection


class RawExplorer(App):
    title = "Dwarf Fortress Raw Explorer"
    raws = kpt.ObjectProperty()

    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # Get tabs for the main content window
        self.tabs = TabbedPanel()
        self.views = [CreatureView(app=self)]
        for view in self.views:
            self.tabs.add_widget(view)
        self.tabs.set_def_tab(self.views[0])

        # Create a menu bar at the top
        menuheight = 30
        self.menu = BoxLayout(orientation="horizontal",
                              size_hint=(None, None), size=(200, menuheight))

        self.drops = {}
        self.drops["file"] = DropDown(text="File")
        self.menu.add_widget(self.drops["file"])
        self.drops["file"].add_button(text="Open", func=self.get_file)
        self.drops["file"].add_button(text="Save", func=self.save_raws)
        self.drops["file"].add_button(
            text="Exit", func=lambda btn: self.stop())

        # Automatically populate the Scripts dropdown with anything found in the scripts folder
        self.drops["scripts"] = DropDown(text="Scripts")
        self.menu.add_widget(self.drops["scripts"])
        self.scripts = import_scripts(self)
        for s in self.scripts:
            self.drops["scripts"].add_widget(s)
            s.bind(on_release=self.drops["scripts"].drop.select)
        self.drops["scripts"].drop.bind(on_select=self.refresh)

        # Add top-level widgets in the appropriate order
        self.root.add_widget(self.menu)
        self.root.add_widget(self.tabs)

    def refresh(self, *largs):
        for view in self.views:
            view.refresh_selected()

    def get_file(self, *largs):
        root = tk.Tk()
        root.withdraw()
        raw_dir = tk.filedialog.askdirectory()
        if os.path.isdir(raw_dir):
            self.raws = RawCollection(path=raw_dir)

        for view in self.views:
            view.refresh_files()
        root.destroy()

    def save_raws(self, *largs):
        if self.raws:
            self.raws.save_raws()
