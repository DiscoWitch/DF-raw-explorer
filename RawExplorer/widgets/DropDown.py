import kivy.uix.dropdown as kdd
import kivy.uix.button as kbutton
import kivy.properties as kpt


class DropDown(kbutton.Button):
    def __init__(self, **kwargs):
        super(DropDown, self).__init__(**kwargs)
        if 'height' not in kwargs:
            self.height = 30
        self.drop = kdd.DropDown()
        self.bind(on_release=self.drop.open)

    def add_button(self, func=None, **kwargs):
        b = kbutton.Button(**kwargs)
        b.size_hint_y = None
        if 'height' not in kwargs:
            b.height = self.height
        b.bind(on_release=self.drop.select)
        if func is not None:
            b.bind(on_release=func)
        self.drop.add_widget(b)
        return b

    def add_widget(self, widget, *largs):
        widget.size_hint_y = None
        return self.drop.add_widget(widget, *largs)

    drop = kpt.ObjectProperty()
    buttons = kpt.AliasProperty(getter=lambda: self.drop.children)
