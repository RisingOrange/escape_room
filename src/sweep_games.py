from asciimatics.event import MouseEvent
from asciimatics.screen import Screen
from .game_utils import *
from .utils import get_active_window_rect
import random

bugs = [
    '''\(")/
-( )-
/(_)\\''',
    ''' __     ,
(__).o.@c
 /  |  \  ''',
    '''  __         
_/__)   
(8|)_}}-
`\__)  ''',
    '''  ,,
  oo
 /==\\
(/==\)
  \/  ''',
    '''    .----.   @   @
   / .-"-.`.  \\v/
   | | '\ \ \_/ )
 ,-\ `-.' /.'  /
'---`----'----'''
]


def overlap(b1, b2): return not (b1[2] < b2[0] or b2[2] < b1[0] or b1[3] < b2[1] or b2[3] < b1[1])


def game1(screen: Screen):
    #update_gun_ui('😃', '︻デ═一', 3)
    # '😃 ︻デ═一', 'ノ'

    random.shuffle(bugs)

    screen.clear_buffer(0, 0, 0)
    intro_msg = 'During the game:\n\n<Press C for controls>\n<Press H for a hint>'
    start_msg = '<Press any key to start>'
    display_help(screen, intro_msg)
    await_continue(screen, screen.width // 2 - len(start_msg) // 2, screen.height // 2 + 5, cont_msg=start_msg)

    clear_condition_met = False

    reticle_x, reticle_y = 0, 0
    restart_mouse_tracking()
    controls_msg = 'MouseMove - Move cursor\nL.Click - Fire\nKeep mouse still while clicking'

    screen.clear()

    num_bugs = 5

    bug_boxes = []  # defines the boundries of the box
    game_bugs = []

    w, h = 150, 40

    for i in range(num_bugs):
        bug_str = bugs[i % len(bugs)]
        bug = bug_str.split('\n')
        bug_w, bug_h = len(max(bug, key=len)), len(bug)
        x, y = random.randint(0, w - bug_w - 1), random.randint(0, h - bug_h - 1)
        tbox = [x, y, x + bug_w, y + bug_h]

        valid = True

        for box in bug_boxes:
            if overlap(box, tbox):
                valid = False
                break

        while not valid:
            x, y = random.randint(0, w - bug_w - 1), random.randint(0, h - bug_h - 1)
            tbox = [x, y, x + bug_w, y + bug_h]

            valid = True

            for box in bug_boxes:
                if overlap(box, tbox):
                    valid = False
                    break

        bug_boxes.append(tbox)
        game_bugs.append(bug_str)

    helps = [
        "Just point and click at the bugs, it's really not that hard to figure out"
    ]

    while not clear_condition_met:
        screen.clear_buffer(0, 0, 0)

        if screen.has_resized():
            restart_mouse_tracking()

        for i in range(len(bug_boxes)):
            to_draw = game_bugs[i].split('\n')
            for y, l in enumerate(to_draw):
                screen.print_at(l, bug_boxes[i][0], bug_boxes[i][1] + y)

        event = screen.get_event()

        fired = False
        got_hint = False
        got_controls = False

        while event is not None:  # catch up to past events
            if isinstance(event, MouseEvent):
                reticle_x, reticle_y = event.x, event.y
                if event.buttons == 1:
                    fired = True
            if isinstance(event, KeyboardEvent):
                key_char = chr(event.key_code).lower()
                if key_char == 'c':
                    got_controls = True
                if key_char == 'h':
                    got_hint = True

            event = screen.get_event()

        if got_controls:
            screen.clear_buffer(0, 0, 0)
            display_help(screen, controls_msg)
            await_continue(screen, screen.width // 2 - 27 // 2, screen.height // 2 + 5)

        if got_hint:
            cont_msg = '<Press H for another hint. Press any other key to continue>'
            for i, hint in enumerate(helps):
                screen.clear_buffer(0, 0, 0)
                display_help(screen, hint)
                screen.print_at(cont_msg, screen.width // 2 - len(cont_msg) // 2, screen.height // 2 + 6)
                screen.refresh()

                if i != len(helps) - 1:
                    h = await_key(screen, 'h')
                    if not h:
                        break

            cont_msg = ' ' * len(cont_msg)
            screen.print_at(cont_msg, screen.width // 2 - len(cont_msg) // 2, screen.height // 2 + 6)
            # cont_msg = '<Press any key to continue>'
            # screen.print_at(cont_msg, screen.width // 2 - len(cont_msg) // 2, screen.height // 2 + 6)
            # screen.refresh()
            # await_key(screen, 'b')
            await_continue(screen, screen.width // 2 - 27 // 2, screen.height // 2 + 6)

        if fired:
            for i, box in enumerate(bug_boxes):
                if box[0] <= reticle_x <= box[2] and box[1] <= reticle_y <= box[3]:
                    bug_boxes.pop(i)
                    game_bugs.pop(i)
                    break

        draw_reticle(screen, reticle_x, reticle_y)
        screen.refresh()

        clear_condition_met = len(game_bugs) == 0


def game2(screen: Screen):
    _, _, w, h = get_active_window_rect()
    tile_width, tile_height = w / screen.width, h / screen.height

    mw, mh = get_monitor_size()
    monitor_width, monitor_height = int(mw / tile_width), int(mh / tile_height)
    bx1, by1 = 10, screen.height // 2
    bx2, by2 = monitor_width - 10, monitor_height - 10

    num_bugs = 5

    bug_boxes = []  # defines the boundries of the box
    game_bugs = []

    for i in range(num_bugs):
        bug_str = bugs[i % len(bugs)]
        bug = bug_str.split('\n')
        bug_w, bug_h = len(max(bug, key=len)), len(bug)
        x, y = random.randint(bx1, bx2 - 1), random.randint(by1, by2 - 1)
        tbox = [x, y, x + bug_w, y + bug_h]

        valid = True

        for box in bug_boxes:
            if overlap(box, tbox):
                valid = False
                break

        while not valid:
            x, y = random.randint(bx1, bx2 - 1), random.randint(by1, by2 - 1)
            tbox = [x, y, x + bug_w, y + bug_h]

            valid = True

            for box in bug_boxes:
                if overlap(box, tbox):
                    valid = False
                    break

        bug_boxes.append(tbox)
        game_bugs.append(bug_str)

    screen.clear()

    reticle_x, reticle_y = screen.width // 2, screen.height // 2

    clear_condition_met = False

    controls_msg = 'Move reticle - Move reticle\nSpace - Fire'
    helps = [
        'The box\'s pretty light and you\'re quite strong;\nwhy not move the box around?',
        'You\'re surrounded by boxes, and there are some boxes\nthat contain other boxes,\nlike the one you\'re staring at right now',
        "Windows are box shaped, wouldn't you agree?",
        "I am inside a window."
    ]

    while not clear_condition_met:
        screen.clear_buffer(0, 0, 0)

        fired = False
        got_hint = False
        got_controls = False

        event = screen.get_event()

        while event is not None:  # catch up to past events
            if isinstance(event, KeyboardEvent):
                key_char = chr(event.key_code).lower()
                if key_char == 'c':
                    got_controls = True
                if key_char == 'h':
                    got_hint = True
                if key_char == ' ':
                    fired = True

            event = screen.get_event()

        if got_controls:
            screen.clear_buffer(0, 0, 0)
            display_help(screen, controls_msg)
            await_continue(screen, screen.width // 2 - 27 // 2, screen.height // 2 + 5)

        if got_hint:
            cont_msg = '<Press H for another hint. Press any other key to continue>'
            for i, hint in enumerate(helps):
                screen.clear_buffer(0, 0, 0)
                display_help(screen, hint)
                screen.print_at(cont_msg, screen.width // 2 - len(cont_msg) // 2, screen.height // 2 + 6)
                screen.refresh()

                if i != len(helps) - 1:
                    h = await_key(screen, 'h')
                    if not h:
                        break

            cont_msg = ' ' * len(cont_msg)
            screen.print_at(cont_msg, screen.width // 2 - len(cont_msg) // 2, screen.height // 2 + 6)
            cont_msg = '<Press any key to continue>'
            screen.print_at(cont_msg, screen.width // 2 - len(cont_msg) // 2, screen.height // 2 + 6)
            screen.refresh()
            await_key(screen, 'b')

        x, y, _, _ = get_active_window_rect()
        tiled_x, tiled_y = int(x / tile_width), int(y / tile_height)

        for i in range(len(bug_boxes)):
            to_draw = game_bugs[i].split('\n')
            for y, l in enumerate(to_draw):
                screen.print_at(l, bug_boxes[i][0] - tiled_x, bug_boxes[i][1] + y - tiled_y)

        draw_reticle(screen, reticle_x, reticle_y)

        if fired:
            for i, box in enumerate(bug_boxes):
                if box[0] <= reticle_x + tiled_x <= box[2] and box[1] <= reticle_y + tiled_y <= box[3]:
                    bug_boxes.pop(i)
                    game_bugs.pop(i)
                    break

        screen.refresh()

        clear_condition_met = len(game_bugs) == 0
