import re

from kivy.uix.textinput import TextInput
import kivy.properties as kpt


class EdText(TextInput):
    owner = kpt.ObjectProperty()
    index = kpt.NumericProperty((0, 'in'))

    def __init__(self, **kwargs):
        super(EdText, self).__init__(**kwargs)
        self.multiline = False

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


class FloatInput(EdText):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class IntInput(EdText):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        s = re.sub(self.pat, '', substring)
        return super(IntInput, self).insert_text(s, from_undo=from_undo)
