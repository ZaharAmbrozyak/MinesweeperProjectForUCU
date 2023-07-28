import random
import numpy as np

UNEXPLORED = 'default'
FLAG = 'flag'
EMPTY = 'E'
MINE = 'M'


class Game:
    def __init__(self, size: tuple, num_of_mines: int):
        self.size = size
        self.num_of_mines = num_of_mines
        self.game_board = None
        self.nums_board = None
        self.player_board = np.full(self.size, UNEXPLORED)
        self.end_game = False
        self.first_click = True
        self.mine_poses = []
        self.flag_poses = []
        self.unexplored_poses = [(x, y) for x in range(self.size[0]) for y in range(self.size[1])]

    def setup(self, first_click_pos: tuple = (0, 0)) -> None:
        self.game_board = self.generate_board(first_click_pos)
        self.nums_board = self.generate_neighbors_board()

    def generate_board(self, first_click_pos: tuple) -> np.ndarray:
        temp_board = np.full([self.size[0], self.size[1]], EMPTY)
        available_pos_for_mines = [(x, y) for x in range(self.size[0]) for y in range(self.size[1])]
        first_positions = [(x, y)
                           for x in
                           range(first_click_pos[0] - (self.size[0] + 3) // 4,
                                 first_click_pos[0] + (self.size[0] + 3) // 4)
                           for y in
                           range(first_click_pos[1] - (self.size[1] + 3) // 4,
                                 first_click_pos[1] + (self.size[1] + 3) // 4)]

        available_pos_for_mines = [pos for pos in available_pos_for_mines if pos not in first_positions]
        mines_to_be_placed = self.num_of_mines

        while mines_to_be_placed > 0:
            rand_pos = random.choice(available_pos_for_mines)
            temp_board[rand_pos[0], rand_pos[1]] = MINE
            mines_to_be_placed -= 1
            self.mine_poses.append(rand_pos)
            available_pos_for_mines.remove(rand_pos)
        return temp_board

    def generate_neighbors_board(self) -> np.ndarray:
        neighbors_board_dict = {}

        for x, row in enumerate(self.game_board):
            for y, value in enumerate(row):
                neighbors_board_dict[(x, y)] = neighbors_board_dict.get((x, y), 0)
                if self.game_board[x, y] == MINE:
                    neighbors_board_dict[(x, y)] = 9
                    continue
                for i in [x - 1, x, x + 1]:
                    for j in [y - 1, y, y + 1]:
                        if i < 0 or i > (len(self.game_board) - 1) or j < 0 or j > (len(row) - 1):
                            continue
                        if self.game_board[i, j] == MINE:
                            neighbors_board_dict[(x, y)] = neighbors_board_dict.get((x, y)) + 1

        neighbors_list = np.zeros(self.game_board.shape)
        for key, value in neighbors_board_dict.items():
            neighbors_list[key[0], key[1]] = value
        return neighbors_list

    def print_board(self, board) -> None:
        view = ""
        view += f"   {str([i + 1 for i in range(len(board))])[1:-1].replace(',', '')}\n\n"
        for x in range(len(board[0])):
            view += f"{x + 1}  "
            for y in range(len(board)):
                view += str(board[y, x]) + " "
            view += f"  {x + 1}\n"
        view += f"\n   {str([i + 1 for i in range(len(board))])[1:-1].replace(',', '')}\n"
        print(view)

    def expand_empty_cells(self, pos: tuple) -> None:
        (x, y) = pos
        if self.nums_board[x, y] != 0:
            return
        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                if (i == x and j == y) or i < 0 or i > self.size[0] - 1 or j < 0 or j > self.size[1] - 1:
                    continue
                if self.player_board[i, j] == UNEXPLORED:
                    self.player_board[i, j] = self.nums_board[i, j]
                    self.unexplored_poses.remove((i, j))
                    self.expand_empty_cells((i, j))

    def num_of_left_mines(self) -> int:
        return np.count_nonzero(self.game_board == MINE)

    def reveal_player_board(self) -> None:
        for x, row in enumerate(self.game_board):
            for y, cell in enumerate(row):
                if cell == MINE:
                    self.player_board[x, y] = MINE
                    continue
                self.player_board[x, y] = self.nums_board[x, y]
        self.print_board(self.player_board)

    def do_action(self, cell_choice: tuple, action: str) -> None:
        # cell_choice = tuple(
        #     [int(coord) - 1 for coord in input("What cell to choose?(x, y) ").replace(' ', '').split(',')])
        # action = input("What do you want to do?[open(o)/flag(f)/remove flag(r)] ")
        if self.first_click:
            self.setup(cell_choice)
            self.first_click = False

        if action == 'o':
            if self.game_board[cell_choice[0], cell_choice[1]] == MINE:
                # print("You lost!")
                self.end_game = True
            elif self.player_board[cell_choice[0], cell_choice[1]] == UNEXPLORED:
                # print("Cell opened")
                num_of_near_mines = self.nums_board[cell_choice[0], cell_choice[1]]
                self.player_board[cell_choice[0], cell_choice[1]] = num_of_near_mines
                self.expand_empty_cells(cell_choice)
                self.unexplored_poses.remove(cell_choice)
        elif action == 'f':
            self.player_board[cell_choice[0], cell_choice[1]] = FLAG
            self.flag_poses.append(cell_choice)
        elif action == 'r' and self.player_board[cell_choice[0], cell_choice[1]] == FLAG:
            self.player_board[cell_choice[0], cell_choice[1]] = UNEXPLORED
            self.flag_poses.remove(cell_choice)
        # else:
            # print("Wrong action or cell choice!")

        can_win = True

        for mine in self.mine_poses:
            # if mine not in self.flag_poses:
            #     can_win = False
            #     break
            if mine not in self.unexplored_poses or len(self.mine_poses) != len(self.unexplored_poses):
                print(len(self.mine_poses), len(self.unexplored_poses))
                can_win = False
                break

        if can_win:
            print("You won!!!\n")
            self.end_game = True
            return
