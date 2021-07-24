import sys
import time
from itertools import product
from random import randint, random

from asciimatics.effects import Print, RandomNoise
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

FRAME_DELAY = 0.15

# amount of correctly typed chars (gets reset to 0 when a wrong char gets typed)
progress = 0

# positions where no noise will show up anymore
disabled_positions = set()

# the next this many frames will be drawn without a delay before them
# calling screen.draw_next_frame() somehow does not show the newest changes, as a workaround a
# couple of frames are drawn without delay right after an update to the scenes was made
no_delay_frame_count = 0


def draw_hints(screen, disabled_positions):
    hint = "try clicking the @-signs"

    for _ in range(100):
        x = randint(-10, screen.width)
        y = randint(-10, screen.height)

        would_cover_disabled_pos = False
        for (x_, y_) in [(x+dx, y) for dx in range(len(hint))]:
            if (x_, y_) in disabled_positions:
                would_cover_disabled_pos = True
                break
        if would_cover_disabled_pos:
            continue

        screen.print_at(hint, x, y)


class MyNoise(RandomNoise):

    def __init__(self, screen, disabled_positions):
        super().__init__(screen)

        self._key_char = '@'
        self._hole_size_x = 7
        self._hole_size_y = 3
        self._disabled_positions = disabled_positions
        self._generate_next = True

    def process_event(self, event):
        if isinstance(event, MouseEvent):
            x, y = event.x, event.y
            char, *_ = self._screen.get_from(x, y)
            if char == ord(self._key_char):
                for dx, dy in product(
                    range(-self._hole_size_x, self._hole_size_x),
                    range(-self._hole_size_y, self._hole_size_y)
                ):
                    self.disable_pos(x+dx, y+dy)

        return super().process_event(event)

    def disable_pos(self, x, y):
        global no_delay_frame_count

        self._screen.print_at(' ', x, y)
        self._disabled_positions.add((x, y))
        no_delay_frame_count = 5

    def update(self, frame_no):
        if not self._generate_next:
            return

        self._generate_next = False
        for y in range(self._screen.height):
            for x in range(self._screen.width):

                if (x, y) in self._disabled_positions:
                    if self._screen.get_from(x, y)[0] == ord(self._key_char):
                        self._screen.print_at(' ', x, y)
                elif random() < 0.2 or self._screen.get_from(x, y)[0] == ord(' '):
                    self._screen.print_at(chr(randint(33, 126)), x, y)

    def update_frame(self):
        self._generate_next = True


def figlet_chars(screen, text, y=2, x=2, colour=Screen.COLOUR_WHITE):
    result = []
    x_ = x
    y_ = y
    for ch in text:
        result.append(
            Print(
                screen,
                FigletText(ch),
                y_,
                x_,
                colour=colour
            )
        )
        if ch == '\n':
            x_ = x
            y_ += 5
        elif ch in 'li ':
            x_ += 2
        else:
            x_ += 6

    return result


def demo(screen):
    global progress, no_delay_frame_count

    noise = MyNoise(screen, disabled_positions)
    main_effects = [
        Print(
            screen,
            FigletText(
                'type this:'),
            2,
            x=2,
        ),
        noise,
    ]
    message = "The box is locked\nThe key is inside"
    message_y = 8
    message_effects = figlet_chars(screen, message, message_y)
    message_effects[:progress] = figlet_chars(screen, message[:progress], colour=Screen.COLOUR_GREEN, y=message_y)
    screen.set_scenes([Scene(main_effects + message_effects)])

    prev_frame_time = time.time() - FRAME_DELAY

    while progress < len(message):
        if screen.has_resized():
            raise ResizeScreenError("")

        event = screen.get_event()
        screen._scenes[0].process_event(event)  # without this the effects wouldnt receive the event
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord(message[progress]):
                progress += 1
                message_effects[:progress] = figlet_chars(
                    screen, message[:progress], colour=Screen.COLOUR_GREEN, y=message_y)
            else:
                # dont break on missing newlines
                if message[progress] == '\n' and progress < len(message)-1 and event.key_code == ord(message[progress+1]):
                    progress += 2
                else:
                    message_effects[:progress] = figlet_chars(
                        screen, message[:progress], colour=Screen.COLOUR_WHITE, y=message_y)
                    progress = 0
            screen.set_scenes([Scene(main_effects + message_effects)])
            no_delay_frame_count = 5

        if time.time() - prev_frame_time > FRAME_DELAY or no_delay_frame_count > 0:
            prev_frame_time = time.time()

            if no_delay_frame_count > 0:
                no_delay_frame_count -= 1

            screen.draw_next_frame()
            noise.update_frame()
            draw_hints(screen, disabled_positions)


def main():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass


if __name__ == '__main__':
    main()
