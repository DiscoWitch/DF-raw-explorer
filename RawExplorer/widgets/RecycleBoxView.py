from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.metrics import dp


class RecycleBoxView(RecycleView):
    def __init__(self, **kwargs):
        super(RecycleBoxView, self).__init__(**kwargs)
        layout = RecycleBoxLayout(default_size_hint=(1, None),
                                  size_hint_y=None,
                                  orientation='vertical')
        layout.bind(minimum_height=layout.setter('height'))
        self.add_widget(layout)
