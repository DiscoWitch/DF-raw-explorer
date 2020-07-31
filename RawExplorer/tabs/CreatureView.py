import json
import os

import kivy.properties as kpt
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.treeview import TreeView, TreeViewLabel

from RawExplorer.widgets.TreeSelect import TreeSelect
from RawExplorer.widgets.TokenView import TokenView
from RawExplorer.widgets.ScrollWrap import ScrollWrap
from RawExplorer.spec import specdir


class CreatureView(TabbedPanelItem):
    app = kpt.ObjectProperty()
    spec = kpt.DictProperty()
    selection = kpt.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Creatures"
        self.create_widgets()

    def create_widgets(self):
        layout = BoxLayout(orientation='horizontal')
        self.add_widget(layout)
        self.sv = ScrollWrap(pos=(0, 0), scroll_type=[
                             'bars'], child=TreeView(hide_root=True))
        self.tokenview = TokenView()
        layout.add_widget(self.sv)
        layout.add_widget(self.tokenview)
        self.refresh_files()

    def refresh_files(self):
        self.spec = {}
        with open(specdir+"/tokens/creature.json", 'r') as f:
            self.spec["tokens"] = json.load(f)
        self.tokenview.rules = self.spec["tokens"]

        if self.app.raws is None:
            return

        creatures = self.app.raws.filter(
            pred_file=lambda f: f.maintype == "CREATURE")
        for fn in creatures.files:
            tree = self.sv.child
            fnode = tree.add_node(TreeViewLabel(text=fn))
            for creature in creatures.files[fn].objects:
                inode = tree.add_node(TreeSelect(text=creature), fnode)
                inode.bind(on_release=self.select_raw)

    def refresh_selected(self):
        if len(self.selection) == 2 \
                and self.selection[0] in self.app.raws.files \
                and self.selection[1] in self.app.raws.files[self.selection[0]].objects:
            self.tokenview.tokens = self.app.raws.files[self.selection[0]
                                                        ].objects[self.selection[1]].tokens
        self.tokenview.update_data()

    # Callback for when a creature entry is selected in the tree
    def select_raw(self, selection):
        self.selection = [selection.parent_node.text, selection.text]
        self.tokenview.tokens = self.app.raws.files[self.selection[0]
                                                    ].objects[self.selection[1]].tokens
