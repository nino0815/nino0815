import curses
import time

EMPTY_LINE = " " * 80
LEVEL = [
    EMPTY_LINE,
    EMPTY_LINE,
    EMPTY_LINE,
    EMPTY_LINE,
    "             X" + " " * 66,
    EMPTY_LINE,
    "      X      X           XX" + " " * 49,
    "==============================    " + "=" * 44,
]

PLAYER_CHAR = "M"


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    width = len(LEVEL[0])
    height = len(LEVEL)

    player_x = 0
    player_y = height - 2
    velocity_y = 0
    on_ground = True

    while True:
        stdscr.clear()
        for y, row in enumerate(LEVEL):
            stdscr.addstr(y, 0, row)
        stdscr.addstr(player_y, player_x, PLAYER_CHAR)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        if key in (curses.KEY_RIGHT, ord('d')):
            if player_x + 1 < width and LEVEL[player_y][player_x + 1] == ' ':
                player_x += 1
        if key in (curses.KEY_LEFT, ord('a')):
            if player_x - 1 >= 0 and LEVEL[player_y][player_x - 1] == ' ':
                player_x -= 1
        if key in (curses.KEY_UP, ord('w'), ord(' ')) and on_ground:
            velocity_y = -2
            on_ground = False

        if not on_ground:
            new_y = player_y + velocity_y
            velocity_y += 1
            if velocity_y > 1:
                velocity_y = 1
            if new_y >= height - 1 or LEVEL[new_y][player_x] != ' ':
                player_y = min(height - 2, player_y + 1)
                on_ground = True
                velocity_y = 0
            else:
                player_y = new_y

        if player_x >= width - 1:
            stdscr.addstr(0, 0, "You win! Press q to quit.")
            stdscr.refresh()
            while stdscr.getch() != ord('q'):
                time.sleep(0.1)
            break
        time.sleep(0.05)


if __name__ == "__main__":
    curses.wrapper(main)
