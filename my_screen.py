import curses


#
#
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

    #Объект секции хранит всю информацию о секции и состояние

#Объекты кнопок (координаты, текст ...)

#Лейблы


#И можно перерисовать полностью уровень из этой информации

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


class Window:
    # ну если не могу понять как работает оверлап, реализую свой объект окна.
    #
    # обатрибуты страт_у старт_х высота ширина
    pass


def copy_section(scr, section_coordinates):
    pass



def menu_window(scr, section_coordinates):
    #
    begin_y = 4 + section_coordinates[0]
    begin_x = 20 + section_coordinates[1]
    height = 15
    width = 40

    menu = curses.newwin(height, width, begin_y, begin_x)

    menu.border()
    menu.addstr(0, 2, 'MENU')
    [menu.addstr(1+y, 1+x, '.') for y in range(height-2) for x in range(width-2)]
    # menu.bkgd('.', curses.color_pair(1))

    menu.overlay(scr)
    menu.noutrefresh()
    scr.noutrefresh(*section_coordinates)
    curses.doupdate()

    while True:
        key = scr.getch()
        if key == curses.KEY_DOWN:
            pass
        elif key == ord('m'):
            # close menu
            # print('AAAAAAAAAAAA')
            menu.clear()
            menu.overlay(scr)
            menu.noutrefresh()
            #
            scr.noutrefresh(*section_coordinates)
            curses.doupdate()

            #
            break



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