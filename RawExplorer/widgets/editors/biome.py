import json

import kivy.properties as kpt
from kivy.uix.spinner import Spinner

from RawExplorer.spec import specdir

biomelist = []

with open(specdir+"/biomelist.json", 'r') as f:
    biomelist = json.load(f)


class Biome(Spinner):
    owner = kpt.ObjectProperty()
    index = kpt.NumericProperty((0, 'in'))

    def __init__(self, **kwargs):
        super(Biome, self).__init__(**kwargs)
        self.values = biomelist

    def tokens_used(self):
        return 1

    def on_index(self, *args):
        ind1 = self.owner.index
        ind2 = int(self.index)
        self.text = self.owner.owner.tokens[ind1][ind2]

    def on_owner(self, *args):
        ind1 = self.owner.index
        ind2 = int(self.index)
        self.text = self.owner.owner.tokens[ind1][ind2]

    def on_text(self, *args):
        ind1 = self.owner.index
        ind2 = int(self.index)
        self.owner.owner.tokens[ind1][ind2] = self.text
