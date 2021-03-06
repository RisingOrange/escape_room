from time import sleep

from asciimatics.effects import BannerText, Mirage, Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import Box, FigletText, Fire, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from .terminal import Terminal

game_fin = False


def demo(screen):

    scenes = []
    effects = [
        Print(screen, Rainbow(screen, FigletText("ESCAPE",
                                                 font='univers', width=screen.width)),
              screen.height//4-5,
              colour=7, speed=10, bg=7 if screen.unicode_aware else 0),
        Print(screen, Rainbow(screen, FigletText("ROOM",
                                                 font='univers', width=screen.width,)),
              screen.height//4+5,
              colour=7, speed=20, bg=7 if screen.unicode_aware else 0),
        Print(screen, Box(screen.width-10, screen.height-6, uni=True), 1, 5, colour=0, speed=30, bg=7),
        Print(screen, FigletText('press X to continue', font='digital', width=screen.width-10),
              screen.height-4, screen.width//4+5, speed=10, transparent=False, start_frame=40),
        Print(screen, FigletText('-------------------', font='digital', width=screen.width-10),
              screen.height-4, screen.width//4+5, speed=20, transparent=False, start_frame=40)
    ]

    scenes.append(Scene(effects, clear=False))
    screen.play(scenes)

    for i in range(screen.height-7):
        for j in range((screen.width-11)//6):
            screen.move(8+6*j, 2)
            screen.draw(8+6*j, 2+i, char='|||')

    screen.refresh()
    sleep(1)

    scenes = []
    effects = [
        BannerText(
            screen,
            Rainbow(screen, FigletText(
                "S T A G E   1 - T H E   B O X U P   P U Z Z L E", font='fourtops')),
            screen.height // 4,
            Screen.COLOUR_GREEN, stop_frame=170),
        Print(screen,
              Fire(screen.height, screen.width, "@" * screen.width, 0.8, 60, screen.colours,
                   bg=screen.colours >= 256),
              0,
              speed=1,
              transparent=True, start_frame=150, stop_frame=170),
        Print(screen, FigletText('press X to continue', font='digital', width=screen.width-10),
              screen.height-4, screen.width//4+5, speed=10, transparent=False, start_frame=170),
        Print(screen, FigletText('-------------------', font='digital', width=screen.width-10),
              screen.height-4, screen.width//4+5, speed=30, transparent=False, start_frame=170),
    ]

    scenes.append(Scene(effects, clear=False))
    screen.play(scenes)

    scenes = []
    effects = [
        Print(screen, FigletText('AIM>', font='standard', width=screen.width//4), 8, 0),
        Mirage(screen, FigletText('Push the small red box inside the big blue box\n\nMove the boxes by pushing from the inside\n\nA small box inside a large box can be pushed together',
               font='term', width=screen.width), screen.height//3, 3),
        Print(screen, FigletText('press X to continue', font='digital', width=screen.width-10),
              screen.height-4, screen.width//4+5, speed=10, transparent=False),
        Print(screen, FigletText('-------------------', font='digital', width=screen.width-10),
              screen.height-4, screen.width//4+5, speed=30, transparent=False)
    ]
    scenes.append(Scene(effects, clear=False))
    screen.play(scenes)


def grid_printer(screen):
    global game_fin

    def cb(string):
        global game_fin

        if string == '53':
            screen.print_at('correct!', 0, 0)
            game_fin = True
        else:
            screen.print_at('wrong', 0, 0)

    terminal = Terminal(screen, cb)
    effects = [
        terminal,
    ]
    screen.set_scenes([Scene(effects)])

    while not game_fin:
        screen.print_at('Enter the SUM OF DIGITS of the minimum number of moves to solve the puzzle ', 12, 4, colour=5)
        for i in range(4):
            screen.move(35, 7+5*i)
            screen.draw(65, 7+5*i, thin=True, char='-', bg=7)
            screen.move(35+10*i, 7)
            screen.draw(35+10*i, 23, thin=True, char='|', bg=7)

        screen.fill_polygon([[(49, 14), (49+3, 14), (49+3, 14+2), (49, 14+2)]])
        screen.fill_polygon([[(57, 13), (64, 13), (64, 17), (57, 17)], [
                            (57, 14), (63, 14), (63, 16), (57, 16)]], colour=1)
        screen.fill_polygon([[(35, 13), (46, 13), (46, 18), (35, 18)], [
                            (36, 13), (45, 13), (45, 17), (36, 17)]], colour=4)

        screen.draw_next_frame()


def main():
    while not game_fin:
        try:
            Screen.wrapper(demo)
            Screen.wrapper(grid_printer)
        except ResizeScreenError:
            pass


if __name__ == '__main__':
    main()
