from time import sleep
from block_n_scroll.screen import PadSection


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

    # def highlight(self):
    #     for y in range(5, 18):
    #         for x in range(2, 22):
    #             self.section.pad.addch(self.section.start_y + y, x, '-')
    #     self.section.pad.noutrefresh(*self.section.section_coordinates)
