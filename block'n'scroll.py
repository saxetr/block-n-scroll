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
WIN_COMBINATIONS = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7})
# section_height = 24

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

    difficult_r = Button(section, 13, 80//2 - len("Random")//2, "???", action=status_unavailable, section=section)

    difficult_despairw = Button(section, 14, 80//2 - len("Random")//2, "Despair", action=status_unavailable, section=section)

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

    # if dbg_mode:
    #     for x in range(0,80,4 ):
    #         for y in range(24):
    #             new_board.pad.addstr(y + new_board.section_coordinates[0], x+new_board.section_coordinates[1], '0')
    #     for y in range(0,24,4):
    #         for x in range(80):
    #             new_board.pad.addstr(y + new_board.section_coordinates[0], x + new_board.section_coordinates[1], '0')

    #
    g = Gameplay(new_board)
    g.start_game()


def result_window():
    pass


class Gameplay:
    """
    пользователь вводит координаты своего хода, компьютер делает случайный ход,
     кто играет крестиками выбирается случайно, если кто-то выиграл – это выводится на экран.
    """
    def __init__(self, section: PadSection):
        self.section = section
        self.player = PlayerController(self, 0) # позиция изменяется в toss
        self.computer = AIController(self, 0)   # позиция изменяется в toss
        self.p1 = None  # X
        self.p2 = None  # 0
        self.current_player = self.p1
        #
        self.board = Board(section)

    def start_game(self):
        self.make_board()
        self.toss()
        # в дальнейшем , вызов хода компьютера происходит из функции хода игрока
        if self.p1 is self.computer:
            curses.napms(300)
            self.p1.place_mark(6)   # ячейка рандомно выбирается в методе класса
            curses.napms(300)
            self.p1.place_mark(7)   # ячейка рандомно выбирается в методе класса
            curses.napms(300)
            self.p1.place_mark(8)   # ячейка рандомно выбирается в методе класса


    def make_board(self):
        self.board.draw_grid(3,3)

    def toss(self):
        self.p1 = random.choice((self.player, self.computer))
        # TODO: pytest
        if self.p1 is self.computer:
            self.p2 = self.player
        else:
            self.p2 = self.computer
        #
        self.p1.position = 1
        self.p2.position = 2

    def change_current_player(self):
        if self.current_player is self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1

    def game_loop(self):
        # p1 place_mark
        # p1 win_check  # if win , stop game
        # p2 place_mark
        # p2 wincheck
        pass

    def print_unavailable(self, section, text):
        pass


class Controller:
    def __init__(self, game, position:str):
        self.game = game
        #
        self.moves = set()
        self.position = position

    # place order
    #

    def place_mark(self, mark_coordinates: int):
        min_coord = 1
        max_coord = 9
        if min_coord >= mark_coordinates >= max_coord:
            self.game.print_unavailable(self.game.section, 'out of range')
        #
        cell = self.game.board.cells[mark_coordinates - 1]
        if cell in self.find_empty_cell():
            if self.position == 1:
                cell.draw_x()
            else:
                cell.draw_0()
            #
            self.moves.add(mark_coordinates)
            self.win_check()
        else:
            self.game.print_unavailable(self.game.section, 'cell is busy')

    def find_empty_cell(self):
        """        cell = self.game.board.cells[mark_coordinates - 1]
        :return: список ссылок на ячейки
        """
        empty_cells = []
        for c in self.game.board.cells:
            if c.status == 'empty':
                empty_cells.append(c)
        return empty_cells

    def win_check(self):
        for combo in WIN_COMBINATIONS:
            if combo.issubset(self.moves):
                print(' WIN ' * 40)
            else:
                self.game.change_current_player()


        # GAMEOVER
        if not self.find_empty_cell():
            print(' GAMEOVER' * 20)


class PlayerController(Controller):
    pass


class AIController(Controller):
    def place_mark(self, mark_coordinates: int):
        cell = random.choice(self.find_empty_cell())
        mark_coordinates = self.game.board.cells.index(cell) + 1
        # cell = self.game.board.cells[mark_coordinates - 1]
        print(mark_coordinates)
        #
        if self.position == 1:
            cell.draw_x()
        else:
            cell.draw_0()
        #
        self.moves.add(mark_coordinates)
        print(self.moves)
        self.win_check()


class GridCell:

    n = 1

    def __init__(self, section, start_y, start_x, width, height):
        #
        self.section = section
        self.start_y = start_y
        self.start_x = start_x
        self.height = height
        self.width = width
        #
        self.status_list = ['empty', 'hold_x', 'hold_0']
        self.status = self.status_list[0]
        self.number = self.__class__.n
        #
        self.n = 1
        #
        self.draw_cell()

    def draw_cell(self):
        scr = self.section.pad
        y = self.start_y
        x = self.start_x
        section = self.section
        height = self.height
        width = self.width

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

    def draw_x(self):
        """
        XX   XX
          XXX
        XX   XX
        """
        # XX---XX
        self.section.pad.addch(self.start_y +1, self.start_x + 2, 'X')
        # self.section.pad.addch(self.start_y +1, self.start_x + 3, 'X')
        # self.section.pad.addch(self.start_y +1, self.start_x + 5, 'X')
        self.section.pad.addch(self.start_y +1, self.start_x + 6, 'X')
        # --XXX--
        # self.section.pad.addch(self.start_y +2, self.start_x + 3, 'X')
        self.section.pad.addch(self.start_y +2, self.start_x + 4, 'X')
        # self.section.pad.addch(self.start_y +2, self.start_x + 5, 'X')
        # XX---XX
        self.section.pad.addch(self.start_y +3, self.start_x + 2, 'X')
        # self.section.pad.addch(self.start_y +3, self.start_x + 3, 'X')
        # self.section.pad.addch(self.start_y +3, self.start_x + 5, 'X')
        self.section.pad.addch(self.start_y +3, self.start_x + 6, 'X')
        #
        self.section.pad.refresh(*self.section.section_coordinates)
        #
        self.status = self.status_list[1]

    def draw_0(self):
        """
        --000--
        -0---0-
        --000--
        """
        #
        self.section.pad.addch(self.start_y +1, self.start_x + 3, '0')
        self.section.pad.addch(self.start_y +1, self.start_x + 4, '0')
        self.section.pad.addch(self.start_y +1, self.start_x + 5, '0')
        #
        self.section.pad.addch(self.start_y +2, self.start_x + 2, '0')
        self.section.pad.addch(self.start_y +2, self.start_x + 6, '0')
        #
        self.section.pad.addch(self.start_y +3, self.start_x + 3, '0')
        self.section.pad.addch(self.start_y +3, self.start_x + 4, '0')
        self.section.pad.addch(self.start_y +3, self.start_x + 5, '0')
        #
        self.section.pad.refresh(*self.section.section_coordinates)
        #
        self.status = self.status_list[2]


class Board:
    def __init__(self, section: PadSection):
        self.section = section
        #
        self.cells = []

    def draw_grid(self,  columns: int, raws: int):

        start_y = 3 + self.section.section_coordinates[0]
        start_x = 25 + self.section.section_coordinates[1]

        y = start_y
        x = start_x

        CELL_HEIGHT = 3
        CELL_WIDTH = 7

        for c in range(columns):
            for r in range(raws):
                self.cells.append(GridCell(self.section, y, x, CELL_WIDTH, CELL_HEIGHT))
                x = x + CELL_WIDTH + 3

            y = y + CELL_HEIGHT + 2
            x = start_x

        #
        GridCell.n = 1

    def higlight_computer(self):
        for y in range(5, 18):
            for x in range(2, 22):
                self.section.pad.addch(self.section.start_y + y, x, '-')
        self.section.pad.noutrefresh(*self.section.section_coordinates)


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
