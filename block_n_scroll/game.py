# 2024-02-20
# create by @saxetr


import os
import curses
from time import sleep
from block_n_scroll.screen import PadSection, create_section, scroll_smooth, Button, Label, menu_window
from block_n_scroll.gameplay import Gameplay
from block_n_scroll.enums import VerticalDirection, HorizontalDirection

# section_height = 24


class StartScreen:

    def __init__(self, section, y=9, x=33, width=11, height=5, refresh_sleep_time=0.005) -> None:
        self.section = section
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.s = refresh_sleep_time

    def draw_corner(self, symbol):
        self.section.pad.addstr(self.y, self.x, symbol)
        self.section.pad.refresh(*self.section.section_coordinates)

    def draw_horizontal_line(self, symbol: str, direction: HorizontalDirection):
        for i in range(self.width):
            self.section.pad.addstr(self.y, self.x, symbol)
            if direction == 'right':
                self.x += 1
            else:
                self.x -= 1
            self.section.pad.refresh(*self.section.section_coordinates)
            sleep(self.s)

    def draw_vertical_line(self, symbol, direction: VerticalDirection):
        for i in range(self.height):
            self.section.pad.addstr(self.y, self.x, symbol)
            if direction == 'up':
                self.y += 1
            else:
                self.y -= 1
            self.section.pad.refresh(*self.section.section_coordinates)
            sleep(self.s)

    def go_to_next_section(self):
        # generating s2
        if len(PadSection.list_of_sections) == 1:
            s2 = create_section(self.section.pad, 'difficult_select_screen', prepare_difficult_select)
            scroll_smooth(self.section, s2)
        else:
            scroll_smooth(self.section, PadSection.list_of_sections['difficult_select_screen'])

    def prepare(self):
        #
        start_btn = Button(self.section, "start_btn", 11, 36, "Press F", action=self.go_to_next_section)
        start_btn.draw()
        self.section.pad.addstr(12, 40, "   to start", curses.A_REVERSE)
        self.section.pad.refresh(*self.section.section_coordinates)

        ul_corner = '╔'
        ur_corner = '╗'
        ll_corner = '╚'
        lr_corner = '╝'
        vertical = "║"
        horizontal = "═"

        self.draw_corner(ul_corner)
        self.x += 1

        self.draw_horizontal_line(horizontal, 'right')

        self.draw_corner(ur_corner)
        self.y += 1

        self.draw_vertical_line(vertical, 'down')

        self.draw_corner(lr_corner)
        self.x -= 1

        self.draw_horizontal_line(horizontal, 'left')

        self.draw_corner(ll_corner)
        self.y -= 1

        self.draw_vertical_line(vertical, 'up')

        self.section.pad.move(11, 42)
        self.section.pad.refresh(*self.section.section_coordinates)
        #
        lvl_control_config = {'key_m': (empty_command, 0), 'key_n': (empty_command, 0), 'key_p': (empty_command, 0)}
        self.section.set_config(lvl_control_config)
        print(PadSection.list_of_sections)


def prepare_difficult_select(section: PadSection):
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


def prepare_board(section: PadSection):
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
        # curses.napms(300)

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

    new_board = create_section(section.pad, tag='board_{}'.format(b), make_lvl=prepare_board)
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
    PadSection.current_section = PadSection(pad, 'start_screen')
    PadSection.list_of_sections['start_screen'] = PadSection.current_section
    start_screen = StartScreen(PadSection.current_section)
    start_screen.prepare()

    # set_control
    while True:
        # print(PadSection.current_section.tag)
        PadSection.break_out_flag = False
        level_control(PadSection.current_section)


def run():
    curses.wrapper(main)
