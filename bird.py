import time

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from utils import *

SLEEP_TIME = 0.005

TERMINAL_SIZE = (50, 20)

game_fin = False

def window_relative_pos(screen, x=0, y=0):
    # given a screen object and the position of something (in tiles)
    # calculate the position (in tiles) of an effect so that when the effect is played in the
    # window the effect will stay nearly in the same position on the display if the window
    # is moved
    # x and y are offsets (in tiles) for the effect, when they are both 0 the
    # top left corner of the effect will be at display position (0, 0) (in pixels)
    offset = _window_offset(screen)
    return (x - offset[0], y - offset[1])


def window_global_pos(screen, x=0, y=0):
    # given the position (in tiles) of something relative to the terminal window
    # return it's position (in tiles) on the screen
    offset = _window_offset(screen)
    return (x + offset[0], y + offset[1])


def _window_offset(screen):
    window_rect = get_active_window_rect()
    px_per_tile_width = window_rect[2] / screen.width
    px_per_tile_height = window_rect[3] / screen.height
    result_x = int(window_rect[0] // px_per_tile_width)
    result_y = int(window_rect[1] // px_per_tile_height)
    return (result_x, result_y)


def show_resize_screen(screen, first_time):
    if first_time:
        effects = [
            Print(
                screen,
                FigletText(f"Resize to {TERMINAL_SIZE[0]}x{TERMINAL_SIZE[1]}"),
                y=screen.height//2-3
            ),
        ]
        screen.set_scenes([Scene(effects)])

    screen.print_at(f'current size: {(screen.width, screen.height)}', 0, 0)
    screen.draw_next_frame()


bird_free_string = '''\
   (     
  `-`-.  
  '( @ > 
   _) (  
  /    ) 
 /_,'  / 
   \  /  
   m""m  \
'''

bird_caged_string = '''\
||  |  |   |  ||
||  |  |   |  ||
||  | (|   |  ||
||  |`-|-. |  ||
||  |'(|@ >|  ||
||  | _| ( |  ||
||  |/ |  )|  ||
||  |_,|  /|  ||
||  | \| / |  ||
||==|=m|"m=|==||
||  |  |   |  ||
||  |  |   |  ||\
'''

key_string = '''\
  __       
 /o \_____ 
 \__/-="="`
           \
'''

lock_string = '''
      #######       
    ##      ##     
    ##      ##     
  ##############   
##              ## 
##      ##      ## 
##      ##      ## 
##              ## 
  ##############   
'''

d = {
    'start_pos': None,
    'key_pos': None,
    'found_key': False,
    'opened_lock': False,
}


def add(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1+x2, y1+y2)


def similiar_pos(p1, p2, tolerance):
    x1, y1 = p1
    x2, y2 = p2
    return (
        x1 in range(x2-tolerance, x2+tolerance)
        and y1 in range(y2-tolerance, y2+tolerance)
    )


def center(pos, ascii_art):
    # calculate the position for the left top corner of the ascii art so that
    # the center of it is at pos
    return(
        pos[0] - len(ascii_art.split('\n')[0]) // 2,
        pos[1] - ascii_art.count('\n') // 2,
    )


def main_(screen):
    global game_fin

    CENTER = (screen.width // 2, screen.height // 2)
    OUTSIDE = (-100, -100)

    bird_rpos = (
        5,
        center(CENTER, bird_caged_string)[1],
    )
    lock_rpos = (
        bird_rpos[0] + len(bird_caged_string.split('\n')[0]) + 2,
        bird_rpos[1],
    )
    caged_bird = Print(screen, StaticRenderer([bird_caged_string]), -100)
    free_bird = Print(screen, StaticRenderer([bird_free_string]), -100)
    lock = Print(screen, StaticRenderer([lock_string]), -100)
    key = Print(screen, StaticRenderer([key_string]), -100)
    effects = [
        caged_bird,
        free_bird,
        key,
        lock,
    ]

    if d['start_pos'] is None or d['key_pos'] is None:
        d['start_pos'] = window_global_pos(screen)

        gpos = window_global_pos(screen)
        if gpos[0] >= 6 or gpos[1] >= 6:
            d['key_pos'] = (4, 4)
        else:
            d['key_pos'] = (100, 5)

    main_scenes = [Scene(effects)]
    screen.set_scenes(main_scenes)

    current_scene = None
    win_time = None
    while True:

        if screen.has_resized():
            raise ResizeScreenError("")

        if not similiar_pos((screen.width, screen.height), TERMINAL_SIZE, 2):
            show_resize_screen(screen, current_scene != 'resize')
            current_scene = 'resize'
            continue

        if current_scene != 'main':
            screen.set_scenes(main_scenes)
            current_scene = 'main'

        screen.clear_buffer(Screen.COLOUR_WHITE, 0, Screen.COLOUR_BLACK)

        p = window_relative_pos(screen, *d['start_pos'])

        if not d['opened_lock']:
            screen.print_at(" Help the bird to escape!", *add(p, (2, 1)))
            caged_bird._x, caged_bird._y = add(p, bird_rpos)
            lock._x, lock._y = add(p, lock_rpos)

        key_rpos = window_relative_pos(screen, *d['key_pos'])
        if similiar_pos(key_rpos, CENTER, 14):
            d['found_key'] = True
        if not d['found_key']:
            key._x, key._y = key_rpos
        else:
            key._x, key._y = center(CENTER, key_string)
            if similiar_pos((key._x, key._y), (lock._x, lock._y), 5):
                d['opened_lock'] = True
            if d['opened_lock']:
                if win_time is None:
                    win_time = time.time()
                elif time.time() - win_time > 3:
                    break
                else:
                    lock._x, lock._y = OUTSIDE
                    caged_bird._x, caged_bird._y = OUTSIDE
                    key._x, key._y = OUTSIDE
                    free_bird._x, free_bird._y = add(p, bird_rpos)
                    screen.print_at(" You did it!", *add(p, (2, 1)))

        screen.draw_next_frame()
        time.sleep(SLEEP_TIME)

    game_fin = True


def main():
    while not game_fin:
        try:
            Screen.wrapper(main_)
        except ResizeScreenError:
            pass

if __name__ == '__main__':
    main()