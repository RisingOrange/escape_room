import time

from . import pygetwindow as gw


def get_active_window_rect():
    try:
        get_active_window_rect.last_result = gw.getActiveWindow().box
        return get_active_window_rect.last_result
    except Exception:
        return get_active_window_rect.last_result


get_active_window_rect.last_result = [0, 0, 100, 100]


if __name__ == '__main__':
    while True:
        cur = get_active_window_rect()
        print(cur)
        time.sleep(1)
