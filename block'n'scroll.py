# КОПИРАЙТ
# 2024-02-20
# create by @saxetr


from time import sleep
import os, shutil
import curses, _curses, curses.panel
from curses import wrapper
import random
from my_screen import *


#
# print(shutil.get_terminal_size())

#
#

section_height = 24
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
    while 1:
        key = scr.getch()
        if key == ord('f') or key == ord('F'):
            # scr.clear()

            # # generating s2
            s2 = create_section(scr, 'difficult_select_screen', lvl_difficult_select)
            #
            scroll_smooth(s1, s2)
            break


def lvl_difficult_select(section):
    select_difficult = Label(section, 10,
                             80 // 2 - len("Use N and P keys to select mode and press ENTER:") // 2,
                             "Use N and P keys to select mode and press F:")

    difficult_random = Button(section, 12, 80//2 - len("Random")//2, "Random", action=create_new_board, section=section)

    difficult_random = Button(section, 13, 80//2 - len("Random")//2, "???", action=status_unavailable, section=section)

    difficult_random = Button(section, 14, 80//2 - len("Random")//2, "Despair", action=status_unavailable, section=section)

    lvl_control_config = {'n': PadSection.next_btn}


def lvl_create_board(section):
    Label(section, 1, 80 // 2 - len(section.tag) // 2, section.tag)

    Label(section, 3, 7, 'COMPUTER')
    Label(section, 3, 64, os.getlogin())


def level_control(section: PadSection, dict=0, hide=False, focus=0):
    """
    Обрабатывает пользовательский ввод, вызывается на каждом УРОВНЕ

    """

    b_hide = hide

    # if not b_hide:
    #     Label(section, 19, 65, 'RIGHT : CHANGE')
    #     Label(section, 20, 65, 'LEFT  : CHANGE')
    #     Label(section, 21, 65, 'ENTER : SELECT')

    if section.buttons:
        section.t_set_focus(focus)

    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()



    # нужно передать кнопка-описание-{команда}
    #
    while not PadSection.break_out_flag:
        key = section.pad.getch()
        if key == curses.KEY_ENTER:
            # execute_command(command, kwargs)
            pass

        elif key == curses.KEY_BACKSPACE:
            # выполнить команду(команда)
            # если кнопка на уровне не нужна, передается команда pass_command():pass
            # набор необходимых команд формируется на Уровне( локальные функции , dict, etc...)
            execute_command(status_unavailable, section)

        elif key == ord('f') or key == ord('F'):
            # выполняет команду кнопки с фокусом размещенной в section
            section.t_play_action()

        elif key == ord('1'):
            print("I pressed 1")

        elif key == ord('2'):
            print("I pressed 2")

        elif key == ord('m'):
            menu_window(section)

        elif key == ord('n'):
            execute_command(PadSection.next_btn, self=section)

        elif key == ord('p'):
            section.prev_btn()

        elif key == ord('q'):
            scroll_smooth(section, s1)
            # break


def execute_command(command, **kwargs):
    command(**kwargs)


# command
def empty_command(**kwargs):
    pass
    print("I pressed p")


# command
def status_unavailable(**kwargs):
    section = kwargs['section']
    t = 'Unavailable'

    Label(section, 23, 79-len(t), t)
    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()

    curses.napms(1000)

    Label(section, 23, 79-len(t), ' '*len(t))

    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()


# command
def create_new_board(**kwargs):
    global b
    b = 1

    section = kwargs['section']

    new_board = create_section(section.pad, tag='board_{}'.format(b), make_lvl=lvl_create_board)
    b += 1
    scroll_smooth(section, new_board)

    # for x in range(0,80,4 ):
    #     for y in range(24):
    #         new_board.pad.addstr(y + new_board.section_coordinates[0], x+new_board.section_coordinates[1], '0')
    # for y in range(0,24,4):
    #     for x in range(80):
    #         new_board.pad.addstr(y + new_board.section_coordinates[0], x + new_board.section_coordinates[1], '0')


    Gameplay(new_board)



def result_window():
    pass


class Gameplay:
    """
    пользователь вводит координаты своего хода, компьютер делает случайный ход,
     кто играет крестиками выбирается случайно, если кто-то выиграл – это выводится на экран.
    """
    def __init__(self, section: PadSection):
        self.player = set()
        self.computer = set()
        self.p1 = None  # X
        self.p2 = None  # 0

        self.board = Board(section, 3, 3)   # Board init отрисовывает доску

        self.toss()

    def toss(self):
        self.p1 = random.choice((self.player, self.computer))
        # TODO: pytest
        if self.p1 is self.computer:
            self.p2 = self.player
        else:
            self.p2 = self.computer

    def place_mark(self, mark_coodinates):
        # check cell
        if self.board.cells[mark_coodinates-1].status == 'empty':
            print(self.board.cells[mark_coodinates-1].status)
        else:
            print(self.board.cells[mark_coodinates-1].status)

    def set_current_player(self):
        pass



class Controller:

    def win_check(self):
        pass


class PlayerController(Controller):
    pass


class AIController(Controller):
    pass


class GridCell:

    n = 1

    def __init__(self, section, start_y, start_x, width, height):
        #
        self.status_list = ['empty', 'hold_x', 'hold_0']
        self.status = self.status_list[0]
        self.number = self.__class__.n
        #
        self.n = 1
        #
        self.draw_cell(section, start_y, start_x, width, height)

    def draw_cell(self, section, start_y, start_x, width, height):
        scr = section.pad
        y = start_y
        x = start_x

        sleep_time = 0.002

        # lu_corner = '╔'
        # ru_corner = '╗'
        # ld_corner = '╚'
        # rd_corner = '╝'
        # vertical = "║"
        # horizontal = "═"
        lu_corner = '+'
        ru_corner = '+'
        ld_corner = '+'
        rd_corner = '+'
        vertical = "|"
        horizontal = "-"

        v_h_center = "╬"
        a = "╠ ╦ ╩ ╣"

        # 1
        scr.addstr(y, x, lu_corner)
        x += 1
        scr.refresh(*section.section_coordinates)

        # 2
        for i in range(width):
            scr.addstr(y, x, horizontal)
            x += 1
            scr.refresh(*section.section_coordinates)
            sleep(sleep_time)

        # 3
        scr.addstr(y, x, ru_corner)
        y += 1
        scr.refresh(*section.section_coordinates)

        # 4
        for i in range(height):
            scr.addstr(y, x, vertical)
            y += 1
            scr.refresh(*section.section_coordinates)
            sleep(sleep_time)

        # 5
        scr.addstr(y, x, rd_corner)
        x -= 1
        scr.refresh(*section.section_coordinates)

        # 6
        for i in range(width):
            scr.addstr(y, x, horizontal)
            x -= 1
            scr.refresh(*section.section_coordinates)
            sleep(sleep_time)

        # 7
        scr.addstr(y, x, ld_corner)
        y -= 1
        scr.refresh(*section.section_coordinates)

        # 8
        for i in range(height):
            scr.addstr(y, x, vertical)
            y -= 1
            scr.refresh(*section.section_coordinates)
            sleep(sleep_time)

        # 9
        scr.addstr(y, x+1, str(self.__class__.n))
        self.__class__.n += 1


class Board:
    def __init__(self, section: PadSection, columns: int, raws: int):
        #
        self.cells = []

        #
        self.draw_grid(section, columns, raws)

    def draw_grid(self, section, columns, raws):

        start_y = 3 + section.section_coordinates[0]
        start_x = 25 + section.section_coordinates[1]

        y = start_y
        x = start_x

        CELL_HEIGHT = 3
        CELL_WIDTH = 7

        for c in range(columns):
            for r in range(raws):
                self.cells.append(GridCell(section, y, x, CELL_WIDTH, CELL_HEIGHT))
                x = x + CELL_WIDTH + 3

            y = y + CELL_HEIGHT + 2
            x = start_x

        #
        GridCell.n = 1


# 80x24
def main(stdscr):
    stdscr.keypad(True)

    #
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    #
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    #
    pad = curses.newpad(24*1, 80)
    if dbg_mode:
        for x in range(24*1):
            pad.addstr(x,0, str(x))

    stdscr.refresh()

    # # sections
    global s1
    s1 = PadSection(pad, tag='start_screen')
    lvl_start_screen(pad, s1.section_coordinates)

    # set_control
    while True:
        # print(PadSection.current_section.tag)

        PadSection.break_out_flag = False
        level_control(PadSection.current_section)


    while True:
        # #TODO: игнорировать ввод пока выполняется действие
        key = stdscr.getch()
        if key == curses.KEY_BACKSPACE:
            pass
        elif key == ord('2'):
            scroll_smooth(pad, current_pad_position[0], PadSection.section_count * 23)
        elif key == ord('p'):
            for s in PadSection.list_of_sections:
                print(s)
            print()
            for w in PadSection.list_of_sections['select_mode_screen'].buttons:
                print(w)
        elif key == ord('q'):
            break


if __name__ == '__main__':
    wrapper(main)
