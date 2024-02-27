# КОПИРАЙТ
# 2024-02-20
# create by @saxetr


import os
from curses import wrapper
import random
from my_screen import *

#
WIN_COMBINATIONS = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7})


# section_height = 24


# #
def prepare_lvl__start_screen(section):
    #
    def go_to_next_section():
        # generating s2
        if len(PadSection.list_of_sections) == 1:
            s2 = create_section(section.pad, 'difficult_select_screen', prepare_lvl__difficult_select)
            #
            scroll_smooth(section, s2)
        else:
            scroll_smooth(section, PadSection.list_of_sections['difficult_select_screen'])

    #
    start_btn = Button(section, "start_btn", 11, 36, "Press F", action=go_to_next_section)
    start_btn.draw()
    section.pad.addstr(12, 40, "   to start", curses.A_REVERSE)
    section.pad.refresh(*section.section_coordinates)

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
    section.pad.addstr(y, x, ul_corner)
    x += 1
    section.pad.refresh(*section.section_coordinates)

    # 2
    for i in range(width):
        section.pad.addstr(y, x, horizontal)
        x += 1
        section.pad.refresh(*section.section_coordinates)
        sleep(s)

    # 3
    section.pad.addstr(y, x, ur_corner)
    y += 1
    section.pad.refresh(*section.section_coordinates)

    # 4
    for i in range(height):
        section.pad.addstr(y, x, vertical)
        y += 1
        section.pad.refresh(*section.section_coordinates)
        sleep(s)

    # 5
    section.pad.addstr(y, x, lr_corner)
    x -= 1
    section.pad.refresh(*section.section_coordinates)

    # 6
    for i in range(width):
        section.pad.addstr(y, x, vertical)
        x -= 1
        section.pad.refresh(*section.section_coordinates)
        sleep(s)

    # 7
    section.pad.addstr(y, x, ll_corner)
    y -= 1
    section.pad.refresh(*section.section_coordinates)

    # 8
    for i in range(height):
        section.pad.addstr(y, x, vertical)
        y -= 1

    section.pad.move(11, 42)
    section.pad.refresh(*section.section_coordinates)
    #
    lvl_control_config = {'key_m': (empty_command, 0), 'key_n': (empty_command, 0), 'key_p': (empty_command, 0)}
    section.set_config(lvl_control_config)


def prepare_lvl__difficult_select(section):
    #
    select_difficult = Label(section, 10,
                             80 // 2 - len("Use N and P keys to select mode and press ENTER:") // 2,
                             "Use N and P keys to select mode and press F:")
    select_difficult.draw()
    #
    difficult_random = Button(section, 'random_btn', 12, 80 // 2 - len("Random") // 2,
                              "Random", action=create_new_section_with_board, section=section)
    difficult_random.draw()
    #
    difficult_r = Button(section, 'r_btn', 13, 80 // 2 - len("Random") // 2,
                         "???", action=status_unavailable, section=section)
    difficult_r.draw()
    #
    difficult_despair = Button(section, 'despair_btn', 14, 80 // 2 - len("Random") // 2,
                               "Despair", action=status_unavailable, section=section)
    difficult_despair.draw()


def prepare_lvl__board(section: PadSection):
    # if dbg_mode:
    #     for x in range(0,80,4 ):
    #         for y in range(24):
    #             section.pad.addstr(y + section.section_coordinates[0], x+section.section_coordinates[1], '0')
    #     for y in range(0,24,4):
    #         for x in range(80):
    #             section.pad.addstr(y + section.section_coordinates[0], x + section.section_coordinates[1], '0')

    header = Label(section, 1, 80 // 2 - len(section.tag) // 2, section.tag)
    header.draw()

    c_btn = Button(section, 'computer_btn', 3, 7, ' COMPUTER ')
    c_btn.draw()

    p_btn = Button(section, 'player_btn', 3, 64, os.getlogin())
    p_btn.draw()


def level_control(section: PadSection):
    """
    Обрабатывает пользовательский ввод, вызывается на каждом УРОВНЕ
    
    Вызывается в самом верхнем цикле
    
    забирает конфиг из секции:
        конфиг генерируется в lvl_ функциях или create_section_name функциях и регистрируется в секции


    """

    # if not section.config['hide_legend']:
    #     Label(section, 19, 65, 'RIGHT : CHANGE')
    #     Label(section, 20, 65, 'LEFT  : CHANGE')
    #     Label(section, 21, 65, 'ENTER : SELECT')

    # print("DBG:::LVL_CONTROL:::", section.buttons)
    if section.buttons:
        section.t_set_focus(section.config['focus'])
        # dbg
        # print('DBG:::LVL_CONTROL:::current_focused_btn ', section.current_focused_btn)
        curses.napms(300)

    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()
    # если в секции есть стартовая команда - запустить
    if section.config['start_command']:
        section.config['start_command']()

    # нужно передать кнопка-описание-{команда}
    #
    # #TODO: игнорировать ввод пока выполняется действие
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
        # global?
        elif key == ord('f') or key == ord('F'):
            # выполняет команду кнопки с фокусом размещенной в section
            section.t_play_action()

        elif key == ord('1'):
            execute_command(section.config['key_1'][0], section.config['key_1'][1])
        elif key == ord('2'):
            execute_command(section.config['key_2'][0], section.config['key_2'][1])
        elif key == ord('3'):
            execute_command(section.config['key_3'][0], section.config['key_3'][1])
        elif key == ord('4'):
            execute_command(section.config['key_3'][0], section.config['key_4'][1])
        elif key == ord('5'):
            execute_command(section.config['key_5'][0], section.config['key_5'][1])
        elif key == ord('6'):
            execute_command(section.config['key_6'][0], section.config['key_6'][1])
        elif key == ord('7'):
            execute_command(section.config['key_7'][0], section.config['key_7'][1])
        elif key == ord('8'):
            execute_command(section.config['key_8'][0], section.config['key_8'][1])
        elif key == ord('9'):
            execute_command(section.config['key_9'][0], section.config['key_9'][1])

        # global?
        elif key == ord('m'):
            if section.config['key_m']:
                execute_command(section.config['key_m'][0], section.config['key_m'][1])
            else:
                menu_window(section)

        elif key == ord('n'):
            if section.config['key_n']:
                execute_command(section.config['key_n'][0], section.config['key_n'][1])
            else:
                section.next_btn()

        elif key == ord('p'):
            if section.config['key_p']:
                execute_command(section.config['key_p'][0], section.config['key_p'][1])
            else:
                section.prev_btn()

        elif key == ord('q'):
            scroll_smooth(section, PadSection.list_of_sections['start_screen'])
            # break
            pass


def execute_command(command, *args):
    command(*args)


# command
def empty_command(*args):
    pass


# command
def status_unavailable(**kwargs):
    section = kwargs['section']
    t = 'Unavailable'

    l1 = Label(section, 23, 79 - len(t), t)
    l1.draw()

    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()

    curses.napms(1000)

    l2 = Label(section, 23, 79 - len(t), ' ' * len(t))
    l2.draw()

    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()


# command
def create_new_section_with_board(**kwargs):
    global b
    b = 1

    section = kwargs['section']

    new_board = create_section(section.pad, tag='board_{}'.format(b), make_lvl=prepare_lvl__board)
    b += 1
    scroll_smooth(section, new_board)
    #
    g = Gameplay(new_board)
    #
    new_board.buttons[1].set_action(g.player.place_mark)
    #
    lvl_control_config = {'key_1': (g.player.set_mark_coordinates, 1),
                          'key_2': (g.player.set_mark_coordinates, 2),
                          'key_3': (g.player.set_mark_coordinates, 3),
                          'key_4': (g.player.set_mark_coordinates, 4),
                          'key_5': (g.player.set_mark_coordinates, 5),
                          'key_6': (g.player.set_mark_coordinates, 6),
                          'key_7': (g.player.set_mark_coordinates, 7),
                          'key_8': (g.player.set_mark_coordinates, 8),
                          'key_9': (g.player.set_mark_coordinates, 9),
                          'key_n': (empty_command, 0),
                          'key_p': (empty_command, 0),
                          'hide': False,
                          'start_command': g.start_game}
    new_board.set_config(lvl_control_config)


def result_window():
    pass


class Gameplay:
    """
    пользователь вводит координаты своего хода, компьютер делает случайный ход,
     кто играет крестиками выбирается случайно, если кто-то выиграл – это выводится на экран.
    """

    def __init__(self, section: PadSection):
        #
        self.section = section
        self.player = PlayerController(self, 0)  # позиция изменяется в toss__init
        self.computer = AIController(self, 0)  # позиция изменяется в toss__init
        self.p1 = None  # X
        self.p2 = None  # 0
        #
        self.board = Board(section)
        #
        self.toss__init()  # да, в инит, но столько проблем решает...
        self.current_player = self.p1

    def toss__init(self):
        self.p1 = random.choice((self.player, self.computer))
        # TODO: pytest
        if self.p1 is self.computer:
            self.p2 = self.player
        else:
            self.p2 = self.computer
            # interface
            # устанавливаем фокус на player_btn
            self.section.set_config({'focus': 1})
        #
        self.p1.position = 1
        self.p2.position = 2

    def start_game(self):
        self.make_board()
        # в дальнейшем , вызов хода компьютера происходит из функции хода игрока
        if self.p1 is self.computer:
            curses.napms(1000)
            self.p1.place_mark()

    def make_board(self):
        self.section.set_gameplay(self)
        #
        self.board.draw_grid(3, 3)

    def change_current_player(self):
        if self.current_player is self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1
        # interface
        self.section.next_btn()

    def print_unavailable(self, section, text):
        pass


class Controller:
    def __init__(self, game, position: int):
        self.game = game
        #
        self.moves = set()
        self.position = position

    def find_empty_cell(self):
        """
        :return: список ссылок на ячейки
        """
        empty_cells = []
        for c in self.game.board.cells:
            if c.status == 'empty':
                empty_cells.append(c)
        return empty_cells

    def win_check_and_change_player(self):
        for combo in WIN_COMBINATIONS:
            if combo.issubset(self.moves):
                print(' WIN ' * 40)
                curses.napms(1000)
                exit()

        # GAMEOVER
        if not self.find_empty_cell():
            print(' GAMEOVER' * 20)
            curses.napms(1000)
            exit()
        #
        self.game.change_current_player()


class PlayerController(Controller):
    def __init__(self, game, position: int):
        super().__init__(game, position)
        self.mark_coordinates = None

    def set_mark_coordinates(self, coord: int):
        self.mark_coordinates = coord

        # interface
        l_coord = Label(self.game.section, 8, 60, 'Enter coordinate:')
        l_coord.draw()

        # interface
        m = Label(self.game.section, 9, 65, str(coord))
        m.draw()

        curses.doupdate()

    def place_mark(self):
        if self.mark_coordinates:
            #
            cell = self.game.board.cells[self.mark_coordinates - 1]
            if cell in self.find_empty_cell():
                if self.position == 1:
                    cell.draw_x()
                else:
                    cell.draw_0()
                #
                self.moves.add(self.mark_coordinates)
                self.win_check_and_change_player()
                # вызов метода AIController
                self.game.current_player.place_mark()
            else:
                self.game.print_unavailable(self.game.section, 'cell is busy')


class AIController(Controller):
    def place_mark(self):
        cell = random.choice(self.find_empty_cell())
        mark_coordinates = self.game.board.cells.index(cell) + 1
        # print(mark_coordinates)
        #
        curses.napms(1000)
        if self.position == 1:
            cell.draw_x()
        else:
            cell.draw_0()
        #
        self.moves.add(mark_coordinates)
        # print(self.moves)
        self.win_check_and_change_player()


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
        scr.addstr(y, x + 1, str(self.__class__.n))
        self.__class__.n += 1

    def draw_x(self):
        """
        XX   XX
          XXX
        XX   XX
        """
        # XX---XX
        self.section.pad.addch(self.start_y + 1, self.start_x + 2, 'X')
        # self.section.pad.addch(self.start_y +1, self.start_x + 3, 'X')
        # self.section.pad.addch(self.start_y +1, self.start_x + 5, 'X')
        self.section.pad.addch(self.start_y + 1, self.start_x + 6, 'X')
        # --XXX--
        # self.section.pad.addch(self.start_y +2, self.start_x + 3, 'X')
        self.section.pad.addch(self.start_y + 2, self.start_x + 4, 'X')
        # self.section.pad.addch(self.start_y +2, self.start_x + 5, 'X')
        # XX---XX
        self.section.pad.addch(self.start_y + 3, self.start_x + 2, 'X')
        # self.section.pad.addch(self.start_y +3, self.start_x + 3, 'X')
        # self.section.pad.addch(self.start_y +3, self.start_x + 5, 'X')
        self.section.pad.addch(self.start_y + 3, self.start_x + 6, 'X')
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
        self.section.pad.addch(self.start_y + 1, self.start_x + 3, '0')
        self.section.pad.addch(self.start_y + 1, self.start_x + 4, '0')
        self.section.pad.addch(self.start_y + 1, self.start_x + 5, '0')
        #
        self.section.pad.addch(self.start_y + 2, self.start_x + 2, '0')
        self.section.pad.addch(self.start_y + 2, self.start_x + 6, '0')
        #
        self.section.pad.addch(self.start_y + 3, self.start_x + 3, '0')
        self.section.pad.addch(self.start_y + 3, self.start_x + 4, '0')
        self.section.pad.addch(self.start_y + 3, self.start_x + 5, '0')
        #
        self.section.pad.refresh(*self.section.section_coordinates)
        #
        self.status = self.status_list[2]


class Board:
    def __init__(self, section: PadSection):
        self.section = section
        #
        self.cells = []

    def draw_grid(self, columns: int, raws: int):

        start_y = 3 + self.section.section_coordinates[0]
        start_x = 25 + self.section.section_coordinates[1]

        y = start_y
        x = start_x

        cell_height = 3
        cell_width = 7

        for c in range(columns):
            for r in range(raws):
                self.cells.append(GridCell(self.section, y, x, cell_width, cell_height))
                x = x + cell_width + 3

            y = y + cell_height + 2
            x = start_x

        #
        GridCell.n = 1

    def highlight(self):
        for y in range(5, 18):
            for x in range(2, 22):
                self.section.pad.addch(self.section.start_y + y, x, '-')
        self.section.pad.noutrefresh(*self.section.section_coordinates)


# 80x24
def main(stdscr):
    # stdscr config
    stdscr.keypad(True)
    curses.curs_set(0)
    # curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    # create main pad
    pad = curses.newpad(24 * 1, 80)

    # TODO
    # global dbg_window
    # dbg_window = DBG()

    stdscr.refresh()

    # create first section
    PadSection.current_section = create_section(pad, 'start_screen', prepare_lvl__start_screen)

    # set_control
    while True:
        # print(PadSection.current_section.tag)
        PadSection.break_out_flag = False
        level_control(PadSection.current_section)


if __name__ == '__main__':
    wrapper(main)
