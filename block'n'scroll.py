# КОПИРАЙТ
# 2024-02-20
# create by @saxetr


from time import sleep
import os, shutil
import curses, _curses, curses.panel
from curses import wrapper
import random




#
# print(os.getlogin())
# print(shutil.get_terminal_size())

#
#
current_focused_btn = None
prev_pad_position = None
current_pad_position = (0, 0)
win_combinations = [{1,2,3}, {4,5,6}, {7,8,9}, {1,4,7}, {2, 5, 8}, {3,6,9}, {1,5,9}, {3,5,7}]


# #
def lvl_start_screen(scr, section_coordinates):
    scr.addstr(11, 36, "Press F", curses.A_REVERSE | curses.A_BLINK)
    scr.addstr(12, 40, "   to start", curses.A_REVERSE)
    scr.refresh(*section_coordinates)

    y = 9
    x = 33
    width = 11
    height = 5
    s = 0.005

    ul_corner = '╔'
    ur_corner = '╗'
    ll_corner = '╚'
    lr_corner = '╝'
    vertical = "║"
    horizontal = "═"

    # 1
    scr.addstr(y, x, ul_corner)
    x += 1
    scr.refresh(*section_coordinates)

    # 2
    for i in range(width):
        scr.addstr(y, x, horizontal)
        x += 1
        scr.refresh(*section_coordinates)
        sleep(s)

    # 3
    scr.addstr(y, x, ur_corner)
    y += 1
    scr.refresh(*section_coordinates)

    # 4
    for i in range(height):
        scr.addstr(y, x, vertical)
        y += 1
        scr.refresh(*section_coordinates)
        sleep(s)

    # 5
    scr.addstr(y, x, lr_corner)
    x -= 1
    scr.refresh(*section_coordinates)

    # 6
    for i in range(width):
        scr.addstr(y, x, vertical)
        x -= 1
        scr.refresh(*section_coordinates)
        sleep(s)

    # 7
    scr.addstr(y, x, ll_corner)
    y -= 1
    scr.refresh(*section_coordinates)

    # 8
    for i in range(height):
        scr.addstr(y, x, vertical)
        y -= 1

    scr.move(11, 42)
    scr.refresh(*section_coordinates)
    #
    level_control(scr, section_coordinates, scroll_smooth, scr, s1.start_y, s2.start_y, hide=True)

    #
    # while 1:
    #     key = scr.getch()
    #     if key == ord('f') or key == ord('F'):
    #         # scr.clear()
    #         scroll_smooth(scr, s1.start_y, s2.start_y)
    #         break


def lvl_player_select(scr, section_coordinates):
    #
    Label(scr, 10,
          80//2 - len("Use LEFT and RIGHT arrow to select mode and press ENTER:")//2,
          "Use LEFT and RIGHT arrow to select mode and press ENTER:", section_coordinates)

    #
    Button(scr, 14, 46, "Player VS Player", section_coordinates)
    #
    Button(scr, 14, 22, "Player VS PC", section_coordinates)

    #
    scr.noutrefresh(*section_coordinates)


def mode_select_control(scr, section_coordinates):
    while 'nought':
        key = scr.getch()
        if key == ord('f'):
            scroll_smooth(scr, s2.start_y, s3.start_y)
            break
        elif key == curses.KEY_BACKSPACE:
            print("LEFT")
        elif key == curses.KEY_DOWN:
            print("RIGHT")


def lvl_difficult_select(scr, section_coordinates):
    select_difficult = Label(scr, 10,
                             80 // 2 - len("Select difficult:") // 2,
                             "Select difficult:",
                             section_coordinates)

    difficult_random = Button(scr, 12,
                             80//2 - len("Random")//2,
                             "Random",
                             section_coordinates)

    difficult_random = Button(scr, 13,
                             80//2 - len("Random")//2,
                             "???",
                             section_coordinates)

    difficult_random = Button(scr, 14,
                             80//2 - len("Random")//2,
                             "Despair",
                             section_coordinates)

    scr.noutrefresh(*section_coordinates)

    while True:
        key = scr.getch()
        if key == ord('f'):
            board = create_section(scr, lvl_create_board)
            scroll_smooth(scr, section_coordinates[0], board)
            break
        elif key == curses.KEY_BACKSPACE:
            print("LEFT")
        elif key == curses.KEY_DOWN:
            print("RIGHT")


def lvl_create_board(scr, section_coordinates):
    Label(scr, 10, 10, 'TEST NEW SECTION', section_coordinates)


def scroll_smooth(pad, start=0, end=0):
    if start > end:
        step = -1
        end -=1
    else:
        step = 1
        end +=1

    for y in range(start, end, step):
        speed = 0.02
        if y < start*0.05:
            speed -= y * 0.0001
        elif y > end * 0.90:
            speed += y * 0.0001
        else:
            speed = 0.01

        pad.refresh(y, 0, 0, 0, 23, 80)
        # curses.napms(speed)
        sleep(speed)

        global current_pad_position
        current_pad_position = (end, 0)


def set_cursor(btn):
    # curses.setsyx(pve_btn.start_y, pve_btn.start_x)
    pass


#
#   перенести в PadSection ?
def create_section(scr, make_lvl):
    # resize_window
    scr.resize(PadSection.next_y + 24, 80)
    #
    new_section = PadSection(scr, )
    # example: lvl_create_board
    make_lvl(scr, new_section.section_coordinates)

    # noutrefresh
    scr.noutrefresh(*new_section.section_coordinates)

    return new_section.start_y


def level_control(scr, section_coordinates, command, *args, dict=0, hide=False):
    """
    Обрабатывает пользовательский ввод, вызывается на каждом УРОВНЕ
    :param scr:
    :param section_coordinates:
    :param command:
    :param args:
    :param dict:
    :return:
    """

    b_hide = hide

    if not b_hide:
        Label(scr, 19, 65, 'RIGHT : CHANGE', section_coordinates)
        Label(scr, 20, 65, 'LEFT  : CHANGE', section_coordinates)
        Label(scr, 21, 65, 'ENTER : SELECT', section_coordinates)

        scr.noutrefresh(*section_coordinates)
        curses.doupdate()

    # нужно передать кнопка-описание-{команда}
    # как сделать break при необходимости?
    while True:
        key = scr.getch()
        if key == ord('f') or key == ord('F'):
            execute_command(command, *args)
        elif key == curses.KEY_BACKSPACE:
            # выполнить команду(команда)
            # если кнопка на уровне не нужна, передается команда pass_command():pass
            # набор необходимых команд формируется на Уровне( локальные функции )
            execute_command(empty_command, *args)
        elif key == ord('1'):
            print("I pressed p")
        elif key == ord('2'):
            print("I pressed p")
        elif key == ord('m'):
            # menu
            menu_window(scr, section_coordinates)
        elif key == ord('q'):
            break


def empty_command():
    pass
    print("I pressed p")


def execute_command(command, *args):
    command(args)


def result_window():
    pass


def menu_window(scr, section_coordinates):
    #
    begin_y = 4 + section_coordinates[0]
    begin_x = 10 + section_coordinates[1]
    height = 15
    width = 40


    menu = curses.newwin(height, width, begin_y, begin_x)

    # menu.bkgset

    menu.border()
    menu.addstr(0, 2, 'MENU')

    menu.overlay(scr)
    menu.noutrefresh()
    scr.noutrefresh(*section_coordinates)
    curses.doupdate()

    #tmp
        # window.bkgdset
        # window.border
        # window.box

        # window.subwin
        # window.subpad

        # window.timeout(delay)

        # window.mvwin(new_y, new_x)


class Player:
    pass

    def win_check(self):
        pass


class Widget:
    def __init__(self, window, start_y, start_x, widget_text, section_coordinates):
        self.text = widget_text
        self.start_y = start_y
        self.start_x = start_x
        self.global_start_y = section_coordinates[0] + start_y
        self.global_start_x = section_coordinates[1] + start_x
        # self.end_x =
        self.section_coordinates = section_coordinates
        self.window = window

        #
        self.draw()

    def draw(self, attr=0):
        self.window.addstr(self.global_start_y, self.global_start_x, self.text, attr)
        self.window.noutrefresh(*self.section_coordinates)


class Label(Widget):
    pass


class Button(Widget):
    """
    однострочная кнопка
    """
    def __init__(self, window, start_y, start_x, widget_text, section_coordinates):
        super().__init__(window, start_y, start_x, widget_text, section_coordinates)
        self.is_focused = False

    def draw(self, attr=curses.A_UNDERLINE):
        self.window.addstr(self.global_start_y, self.global_start_x, self.text, attr)
        self.window.noutrefresh(*self.section_coordinates)

    # заместо того, чтоб устанавливать фокус вручную ,
    # нужно устанавливать курсор в границах кнопки, и в этом случае автоматически устанавливать фокус
    def set_focus(self):
        self.is_focused = True
        #
        self.draw(attr=curses.A_REVERSE | curses.A_BLINK)

        global current_focused_btn
        current_focused_btn = self

    def clear_focus(self):
        pass

    def action(self):
        pass


class PadSection:
    #
    section_count = 0
    next_y = 0

    def __init__(self, scr, size_y=23):         # max_line - 1
        self.start_y = self.__class__.next_y
        self.end_y = size_y
        self.end_x = 80
        #
        self.section_coordinates = (self.start_y, 0, 0, 0, self.end_y, self.end_x)
        #
        scr.addstr(self.start_y, 78, "==")
        scr.noutrefresh(*self.section_coordinates)
        #
        self.__class__.next_y += self.end_y + 1
        self.__class__.section_count += 1





class GridCell:
    pass

class Board:
    pass


def draw_cell(scr, start_y, start_x, width, height):
    y = start_y
    x = start_x

    sleep_time = 0.001

    lu_corner = '╔'
    ru_corner = '╗'
    ld_corner = '╚'
    rd_corner = '╝'
    vertical = "║"
    horizontal = "═"

    v_h_center = "╬"
    a = "╠ ╦ ╩ ╣"

    # 1
    scr.addstr(y, x, lu_corner)
    x += 1
    scr.refresh()

    # 2
    for i in range(width):
        scr.addstr(y, x, horizontal)
        x += 1
        scr.refresh()
        sleep(sleep_time)

    # 3
    scr.addstr(y, x, ru_corner)
    y += 1
    scr.refresh()

    # 4
    for i in range(height):
        scr.addstr(y, x, vertical)
        y += 1
        scr.refresh()
        sleep(sleep_time)

    # 5
    scr.addstr(y, x, rd_corner)
    x -= 1
    scr.refresh()

    # 6
    for i in range(width):
        scr.addstr(y, x, horizontal)
        x -= 1
        scr.refresh()
        sleep(sleep_time)

    # 7
    scr.addstr(y, x, ld_corner)
    y -= 1
    scr.refresh()

    # 8
    for i in range(height):
        scr.addstr(y, x, vertical)
        y -= 1
        scr.refresh()
        sleep(sleep_time)


def draw_grid(scr, columns, raws, section_coordinates):


    start_y = 3 + section_coordinates[0]
    start_x = 25 + section_coordinates[1]

    y = start_y
    x = start_x

    CELL_HEIGHT = 3
    CELL_WIDTH = 7

    for c in range(columns):
        for r in range(raws):
            draw_cell(scr, y, x, CELL_WIDTH, CELL_HEIGHT)
            x = x + CELL_WIDTH + 3

        y = y + CELL_HEIGHT + 2
        x = start_x


# 80x24
def main(stdscr):
    stdscr.keypad(True)

    #
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    #
    pad = curses.newpad(24*2, 80)
    for x in range(24*2):
        pad.addstr(x,0, str(x))

    stdscr.refresh()



    # # sections
    global s1, s2, s3
    s1 = PadSection(pad)
    s2 = PadSection(pad)      # lobby
    # s3 = PadSection(pad)
    # # filling s2
    # lvl_player_select(pad, s2.section_coordinates)
    # #
    # curses.doupdate()
    # #
    lvl_start_screen(pad, s1.section_coordinates)
    # #
    # mode_select_control(pad, s2.section_coordinates)
    # #
    # lvl_difficult_select(pad, s3.section_coordinates)
    # curses.doupdate()
    # #
    while True:
        """TODO: игнорировать ввод пока выполняется действие"""
        key = stdscr.getch()
        if key == curses.KEY_BACKSPACE:
            new_board = create_section(pad, lvl_create_board)
            scroll_smooth(pad, current_pad_position[0], new_board)
            # print("I pressed p")
        elif key == ord('1'):
            scroll_smooth(pad, current_pad_position[0], s1.start_y)
        elif key == ord('2'):
            scroll_smooth(pad, current_pad_position[0], PadSection.section_count * 23)
        elif key == ord('q'):
            break


    # # draw_grid(stdscr, 3, 3)

    #
    # stdscr.addstr(1,0, str(type(current_focused_btn)))


if __name__ == '__main__':
    wrapper(main)
