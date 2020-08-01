import importlib
import re
import sys
import os

import kivy.properties as kpt
from kivy.uix.button import Button

scriptdir = os.path.dirname(__file__)


def import_scripts(app):
    files = os.listdir(scriptdir)
    sclasses = []
    for f in files:
        fpath = "{}/{}".format(scriptdir, f)
        if os.path.isfile(fpath) and not f.startswith("_") and f.endswith(".py"):
            name = f[:-3]
            modulepath = "{}.{}".format(__package__, name)
            if modulepath in sys.modules:
                module = sys.modules[modulepath]
            else:
                module = importlib.import_module(modulepath)
            if hasattr(module, name):
                sclasses.append(getattr(module, name))
    scripts = []
    for c in sclasses:
        if issubclass(c, ScriptButton):
            scripts.append(c(app=app))
        else:
            print("{} is not a subclass of ScriptButton".format(c))

    return scripts


class ScriptButton(Button):
    app = kpt.ObjectProperty()

    def __init__(self, **kwargs):
        super(ScriptButton, self).__init__(**kwargs)
        self.halign = "center"
        self.valign = "center"
        self.bind(width=self.setter("text_size[0]"))
        self.text_size[0] = self.width

    def on_texture_size(self, *largs):
        self.height = self.texture_size[1]+5
