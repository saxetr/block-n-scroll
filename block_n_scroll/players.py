import random
import curses
from block_n_scroll.screen import Label


#  TODO не в плеерах должен бытьь
WIN_COMBINATIONS = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7})


class Player:
    def __init__(self, game, mark: str):
        self.game = game
        #
        self.moves = set()
        self.mark = mark

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


class HumanPlayer(Player):
    def __init__(self, game, mark: str):
        super().__init__(game, mark)
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
                if self.mark == 'x':
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


class AIPlayer(Player):
    def place_mark(self):
        cell = random.choice(self.find_empty_cell())
        mark_coordinates = self.game.board.cells.index(cell) + 1
        # print(mark_coordinates)
        #
        curses.napms(1000)
        if self.mark == 'x':
            cell.draw_x()
        else:
            cell.draw_0()
        #
        self.moves.add(mark_coordinates)
        # print(self.moves)
        self.win_check_and_change_player()