from kivy.uix.scrollview import ScrollView
import kivy.properties as kpt


class ScrollWrap(ScrollView):
    child = kpt.ObjectProperty()

    def __init__(self, **kwargs):
        super(ScrollWrap, self).__init__(**kwargs)

    def on_child(self, instance, value):
        self.add_widget(value)
        value.size_hint_y = None
        value.bind(minimum_height=value.setter('height'))
