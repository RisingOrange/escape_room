from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets.frame import Frame
from asciimatics.widgets.layout import Layout
from asciimatics.widgets.text import Text


class Terminal(Frame):

    def __init__(self, screen, callback):
        super().__init__(
            screen,
            height=1,
            width=screen.width,
            y=screen.height-1,
            can_scroll=False,
            has_border=False,
        )
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._text = Text(">", name="input")
        layout.add_widget(self._text)
        self.fix()

        self._callback = callback

    def process_event(self, event):
        if isinstance(event, KeyboardEvent) and event.key_code == ord("\n"):
            self._callback(self._text.value)
            self._text.value = ""
        return super().process_event(event)


def main(screen):
    terminal = Terminal(screen)
    effects = [
        terminal
    ]
    screen.play([Scene(effects)])


if __name__ == '__main__':
    Screen.wrapper(main)
