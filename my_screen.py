import curses
from time import sleep

dbg_mode = True


#
class PadSection:
    #
    section_count = 0
    current_section = None
    next_y = 0

    list_of_sections = {}
    save_section = []

    break_out_flag = False

    def __init__(self, pad, tag: str, size_y=23, legend=True):         # max_line - 1
        self.pad = pad
        self.tag = tag
        self.start_y = self.__class__.next_y
        self.end_y = size_y
        self.end_x = 80
        #
        self.section_coordinates = (self.start_y, 0, 0, 0, self.end_y, self.end_x)
        #
        self.labels = []
        self.buttons = []

        self.current_focused_btn = None
        #
        self.is_legend = legend
        #
        if dbg_mode:
            pad.addstr(self.start_y, 78, "==")
            pad.noutrefresh(*self.section_coordinates)
        #
        self.__class__.next_y += self.end_y + 1
        self.__class__.section_count += 1

    def t_set_focus(self, focus):
        self.buttons[focus].set_focus(self)

    def t_play_action(self):
        cur = self.current_focused_btn
        if cur:
            cur.play_action()
        else:
            pass

    def next_btn(self):
        cur = self.current_focused_btn
        if cur:
            # find button in buttons
            i = self.buttons.index(cur)
            try:
                self.t_set_focus(i + 1)
                cur.clear_focus()
                self.pad.noutrefresh(*self.section_coordinates)
                curses.doupdate()
            except:
                if len(self.buttons) > 1:
                    self.t_set_focus(0)
                    cur.clear_focus()
                    self.pad.noutrefresh(*self.section_coordinates)
                    curses.doupdate()
        else:
            pass

    def prev_btn(self):
        cur = self.current_focused_btn
        if cur:
            # find button in buttons
            i = self.buttons.index(cur)
            try:
                self.t_set_focus(i - 1)
                cur.clear_focus()
                self.pad.noutrefresh(*self.section_coordinates)
                curses.doupdate()
            except:
                if len(self.buttons) > 1:
                    self.t_set_focus(-1)
                    cur.clear_focus()
                    self.pad.noutrefresh(*self.section_coordinates)
                    curses.doupdate()
        else:
            pass

# Объект секции хранит всю информацию о секции и состояние
# Объекты кнопок (координаты, текст ...)
# Лейблы
# И можно перерисовать полностью уровень из этой информации


#
# #TODO   перенести в PadSection ?
def create_section(scr, tag: str, make_lvl):
    # resize_window
    scr.resize(PadSection.next_y + 24, 80)
    #
    new_section = PadSection(scr, tag)
    #
    PadSection.list_of_sections[tag] = new_section
    # example: lvl_create_board
    make_lvl(new_section)

    # noutrefresh
    scr.noutrefresh(*new_section.section_coordinates)

    return new_section


class Window:
    # ну если не могу понять как работает оверлап, реализую свой объект окна.
    #
    # обатрибуты страт_у старт_х высота ширина
    pass


def copy_section(section):
    PadSection.save_section = []
    for y in range(24):
        for x in range(80):
            PadSection.save_section.append(section.pad.inch(y + section.section_coordinates[0],
                                                 x + section.section_coordinates[1]))


def insert_section(section):
    c = 0
    for y in range(24):
        for x in range(80):
            section.pad.insch(y + section.section_coordinates[0],
                              x + section.section_coordinates[1], PadSection.save_section[c])
            c += 1

    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()


def scroll_smooth(from_section: PadSection, to_section: PadSection):

    start = from_section.start_y
    end = to_section.start_y
    pad = from_section.pad

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

    PadSection.current_section = to_section
    # выходим из цикла level_control
    PadSection.break_out_flag = True


def menu_window(section):
    #
    copy_section(section)

    #
    begin_y = 4 + section.section_coordinates[0]
    begin_x = 20 + section.section_coordinates[1]
    height = 15
    width = 40

    menu = curses.newwin(height, width, begin_y, begin_x)

    menu.border()
    menu.addstr(0, 2, 'MENU')
    [menu.addstr(1+y, 1+x, '.') for y in range(height-2) for x in range(width-2)]
    # menu.bkgd('.', curses.color_pair(1))

    menu.overlay(section.pad)
    menu.noutrefresh()
    section.pad.noutrefresh(*section.section_coordinates)
    curses.doupdate()

    while True:
        key = section.pad.getch()
        if key == curses.KEY_DOWN:
            pass
        elif key == ord('m'):
            # close menu
            insert_section(section)
            #
            break

class StatusBar:
    pass


class Widget:
    """

    """
    def __init__(self, area: PadSection, start_y: int, start_x: int, widget_text: str):
        self.text = widget_text
        self.start_y = start_y + area.section_coordinates[0]
        self.start_x = start_x + area.section_coordinates[1]
        # #TODO: нужна прорверка на границы'''
        self.end_y = start_y
        self.end_x = start_x + len(widget_text)
        self.area = area
        #
        self.draw()

    def draw(self, attr=0):
        self.area.pad.addstr(self.start_y, self.start_x, self.text, attr)
        self.area.pad.noutrefresh(*self.area.section_coordinates)


class Label(Widget):
    def __init__(self, area: PadSection, start_y: int, start_x: int, widget_text: str):
        super().__init__(area, start_y, start_x, widget_text)
        #
        area.labels.append(self)


class Button(Widget):
    """

    """
    def __init__(self, area: PadSection, start_y: int, start_x: int, widget_text: str, action, **kwargs):
        super().__init__(area, start_y, start_x, widget_text)
        self.is_focused = False
        self.action = action
        self.kwargs = kwargs

        #
        area.buttons.append(self)

    def draw(self, attr=curses.A_UNDERLINE):
        self.area.pad.addstr(self.start_y, self.start_x, self.text, attr)
        self.area.pad.noutrefresh(*self.area.section_coordinates)

    def set_focus(self, section):
        self.is_focused = True
        #
        self.draw(attr=curses.A_REVERSE | curses.A_BLINK)

        section.current_focused_btn = self

    def clear_focus(self):
        self.is_focused = False
        #
        self.draw(attr=curses.A_UNDERLINE)

    def play_action(self):
        self.action(**self.kwargs)

