from asciimatics.screen import Screen

from .game_utils import display_dialogue, set_screen_size, disable_mouse_tracking
from .sweep_games import game1, game2

worlds = []

game_fin = False

def demo(screen):
    global game_fin

    tw, th = 150, 40
    l = 10

    if abs(screen.width - tw) > l or abs(screen.height - th) > l:
        set_screen_size(screen, (tw, th), leniency=l)
        return

    texts = [
        'Welcome, janitor, to your first and last day at this nuclear power plant!',
        'You\'ll have two tasks today, both involving shooting bugs or something, after which everyone gets to go home.',
        'Understood? Good, now get to work.',
        'Well done. Truly brilliant. Your noscoping was incredible.',
        'Damn it, those children are back. I really hope they don\'t-',
        'Well, it appears the children have stolen your legs. No good. But hey, you still '\
        'have arms.',
        'We\'ll mount you on a robotic frame and you\'ll do more of the same, but not, or something',
        'Nicely done. Now, there\'s one more thing-',
        'Oh no, the children. It would sure be a shame if they-',
        'Good news? The status of your legs has not changed. Bad news? Your '\
        'arms have mysteriously disappeared.',
        'You still have to do your job though, so here\'s a shotgun. Yeah, it\'s '\
        'pretty small, but you\'ll figure something out',
        'Well, uh, I guess you\'re done for the day. Kind of strange how you\'re '\
        'getting paid what, $960,781,132 for a one-time janitorial job? Honestly, '\
        'this sounds like a money-laundering sch-',
        '...',
        'Uh, I\'ll be off. Have a good day sir.'
    ]
    '''
    sprite_sequence = {
        0: [0.45, generate_person(), 0.1, generate_person()],
        5: [0.2, generate_person(small=True), generate_person(small=True), 0.25,
            generate_person(), 0.1, generate_person()],
        6: [0.1, generate_person(small=True), generate_person(small=True), 0.35,
            generate_person(legs=False), 0.1, generate_person()],
        7: [0.45, generate_person(legs=False), 0.1, generate_person()],
        8: [0.2, generate_person(small=True), generate_person(small=True), 0.25,
            generate_person(legs=False), 0.1, generate_person()],
        9: [0.1, generate_person(small=True), generate_person(small=True), 0.35,
            generate_person(legs=False, arms=False), 0.1, generate_person()],
        10: [0.45, generate_person(legs=False, arms=False), 0.1, generate_person()],
    }
    '''
    screen.clear()
    display_dialogue(screen, texts[0:3], box_dimensions=(50, 6))
    game1(screen)
    display_dialogue(screen, texts[3:7], box_dimensions=(50, 6))

    try:
        game2(screen)
    except:
        disable_mouse_tracking()

    display_dialogue(screen, texts[12:], box_dimensions=(50, 6))

    game_fin = True

def main():
    while not game_fin: 
        Screen.wrapper(demo)

if __name__ == '__main__':
    main()