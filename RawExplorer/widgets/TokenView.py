import functools
import importlib
import sys

import kivy.clock
import kivy.properties as kpt
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from .editors.textbox import EdText
from .RecycleBoxView import RecycleBoxView


def get_height(tokens, rules):
    rowheight = 28
    if len(tokens) == 2:
        return rowheight
    else:
        return rowheight*len(tokens)


# Shortcut names for common token types
edit_aliases = {
    "integer": "textbox.IntInput",
    "float": "textbox.FloatInput",
    "string": "textbox.EdText"
}


class TokenSet(BoxLayout):
    owner = kpt.ObjectProperty()
    index = kpt.NumericProperty((0, 'in'), force_dispatch=True)

    def __init__(self, **kwargs):
        super(TokenSet, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [5, 0, 10, 0]

    def get_editor(self, rule, tokens, start_ind):
        t = rule["editor"]
        if t in edit_aliases:
            t = edit_aliases[t]

        if t is None:
            EdClass = TextInput
        else:
            namespace = '.'.join(t.split('.')[:-1])
            classname = t.split('.')[-1]
            modulepath = "{}.editors.{}".format(__package__, namespace)
            if modulepath in sys.modules:
                module = sys.modules[modulepath]
            else:
                module = importlib.import_module(modulepath)
            EdClass = getattr(module, classname)

        editor = EdClass(owner=self, index=start_ind)
        return editor, start_ind+editor.tokens_used()

    def get_editors(self):
        # sys.modules['proj.tabs.CreatureView']
        tokens = self.owner.tokens[self.index]
        if tokens[0] in self.owner.rules:
            rules = self.owner.rules[tokens[0]]
        else:
            rules = None

        rowheight = self.owner.rowheight

        if type(rules) is list:
            desc = Label(
                text=tokens[0], height=rowheight, size_hint_x=None)
            desc.bind(texture_size=desc.setter("size"))
            self.add_widget(desc)
            rows = BoxLayout(orientation="vertical", padding=[20, 0, 0, 0],
                             size_hint_y=None, height=(len(tokens)-1)*rowheight)
            self.add_widget(rows)
            token_ind = 1
            for rule in rules:
                ed = self.get_editor(rule, tokens, token_ind)
                rows.add_widget(ed[0])
                token_ind = ed[1]

        elif type(rules) is dict:
            ed = self.get_editor(rules, tokens, 1)
            self.orientation = 'horizontal'
            desc = Label(text="{}: ".format(tokens[0]), size_hint_x=None)
            desc.bind(texture_size=desc.setter("size"))
            self.add_widget(desc)
            self.add_widget(ed[0])
        else:
            # Boolean tokens: just print
            if len(tokens) == 1:
                self.add_widget(Label(text=tokens[0]))
            # Tokens with one value: inline text entry
            elif len(tokens) == 2:
                self.orientation = 'horizontal'
                desc = Label(text="{}: ".format(tokens[0]), size_hint_x=None)
                desc.bind(texture_size=desc.setter("size"))
                self.add_widget(desc)
                self.add_widget(EdText(owner=self, index=1))
            # Tokens with multiple values: collapsing text entry
            else:
                desc = Label(text=tokens[0], size_hint_x=None)
                desc.bind(texture_size=desc.setter("size"))
                self.add_widget(desc)
                rows = BoxLayout(orientation="vertical", padding=[20, 0, 0, 0],
                                 size_hint_y=None, height=(len(tokens)-1)*rowheight)
                self.add_widget(rows)
                for i in range(1, len(tokens)):
                    rows.add_widget(EdText(owner=self, index=i))

    def on_index(self, *args):
        for child in list(self.children):
            self.remove_widget(child)
        self.orientation = 'vertical'
        self.get_editors()


class TokenView(RecycleBoxView):
    tokens = kpt.ListProperty(force_dispatch=True)
    rules = kpt.DictProperty()
    rowheight = kpt.NumericProperty(28)

    def __init__(self, **kwargs):
        super(TokenView, self).__init__(**kwargs)
        self.viewclass = TokenSet
        self.scroll_type = ['bars']
        self.bar_width = 10
        self.fbind('tokens', self.update_data)
        self.fbind('rules', self.update_data)
        self.fbind('rowheight', self.update_data)

    def update_data(self, *args):
        self.data = [{'owner': self, 'index': i,
                      'height': get_height(self.tokens[i], self.rules)}
                     for i in range(len(self.tokens))]
        self.refresh_from_data()
