import curses
import random
from block_n_scroll.board import Board
from block_n_scroll.screen import PadSection
from block_n_scroll.players import Player, HumanPlayer, AIPlayer


class Gameplay:
    """
    пользователь вводит координаты своего хода, компьютер делает случайный ход,
     кто играет крестиками выбирается случайно, если кто-то выиграл – это выводится на экран.
    """

    def __init__(self, section: PadSection):
        self.section = section
        self.p1: Player | None = None
        self.p2: Player | None = None
        self.current_player: Player | None = None
        self.board = Board(section)

    def create_players(self) -> tuple[Player, Player]:
        player = HumanPlayer(self, '')
        computer = AIPlayer(self, '')

        players = [player, computer]
        random.shuffle(players)

        first, second = players

        first.mark = 'x'
        second.mark = '0'

        if isinstance(first, HumanPlayer):
            self.section.set_config({'focus': 1})

        return first, second

    def init_players(self):
        players = self.create_players()
        self.current_player = players[0]
        self.p1 = players[0]
        self.p2 = players[1]

    def start_game(self):
        self.make_board()
        self.init_players()
        # в дальнейшем , вызов хода компьютера происходит из функции хода игрока
        if isinstance(self.p1, AIPlayer):
            curses.napms(1000)
            self.p1.place_mark()

    def make_board(self):
        self.section.set_gameplay(self)
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