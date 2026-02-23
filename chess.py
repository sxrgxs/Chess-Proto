from abc import ABC, abstractmethod
import random

class GameEngine():

    # Protected:

    def __init__(self):
        self._board = [
            [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' '],
            ['8', '.', '.', '.', '.', '.', '.', '.', '.', '8'],
            ['7', '.', '.', '.', '.', '.', '.', '.', '.', '7'],
            ['6', '.', '.', '.', '.', '.', '.', '.', '.', '6'],
            ['5', '.', '.', '.', '.', '.', '.', '.', '.', '5'],
            ['4', '.', '.', '.', '.', '.', '.', '.', '.', '4'],
            ['3', '.', '.', '.', '.', '.', '.', '.', '.', '3'],
            ['2', '.', '.', '.', '.', '.', '.', '.', '.', '2'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' ']
        ]
        self._curr_state = random.choice(['WHITE', 'BLACK'])

    def get_state(self):
        return self._curr_state

    def set_state(self, state):
        self._curr_state = state

    def _parse_position(self, pos):
        pos = pos.strip().upper()
        col_pos = ord(pos[0]) - ord('A') + 1
        row_pos = ord('8') - ord(pos[1]) + 1

        flag = self._is_inside_board(col_pos, row_pos)

        if not flag:
            raise ValueError

        return col_pos, row_pos

    def _to_position(self, row, col):
        flag = self._is_inside_board(col, row)

        if not flag:
            return False
        return chr(col + 64) + str(9 - row)

    def _is_inside_board(self, col_pos, row_pos):
        if not (1 <= row_pos <= 8 and 1 <= col_pos <= 8):
            return False
        return True

    def _val_move(self, fr, to):
        if self.get_piece(to) is not EMPTY_CELL:
            self.remove_piece(to)

        self.get_piece(fr)._set_position(to)
        self._set_cell(self.get_piece(fr), to)
        self._set_cell('.', fr)
        return 1

    def _set_cell(self, piece, pos):
        col_pos, row_pos = self._parse_position(pos)

        self._board[row_pos][col_pos] = piece
        if type(piece) is not str:
            piece._set_position(pos)

    # Public:

    def add_piece(self, piece, pos):
        if self.get_piece(pos) is not EMPTY_CELL:
            raise ValueError('Cell is already occupied')

        self._set_cell(piece, pos)

    def remove_piece(self, pos):
        piece = self.get_piece(pos)

        if piece is EMPTY_CELL:
            print("Empty cell")
            return None

        self._set_cell('.', pos)
        print(f"Removed piece: {piece.symbol}")

    def get_piece(self, pos):
        col_pos, row_pos = self._parse_position(pos)
        if self._board[row_pos][col_pos] == '.':
            return EMPTY_CELL
        return self._board[row_pos][col_pos]

    def display_board(self):
        for row in range(0, 10):
            for col in range(0, 10):
                if type(self._board[row][col]) is not str:
                    print(self._board[row][col].symbol, end=' ')
                    continue
                print(self._board[row][col], end='　')
            print()

    def move(self, fr, to):
        if self.get_piece(fr) is EMPTY_CELL:
            return

        if to not in self.get_piece(fr).available_moves(self):
            return 0

        self._val_move(fr, to)

    def distribute_pieces(self):
        cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        cell_list = [c + r for r in ['1','2','3','4','5','6','7', '8'] for c in cols]
        random.shuffle(cell_list)
        white_cnt = 0
        black_cnt = 0
        pieces = {
            'WHITE': [(King, random.randint(1, 4)), (Queen,  random.randint(1, 4)), (Knight, random.randint(1, 4))],
            'BLACK': [(King, random.randint(1, 4)), (Queen,  random.randint(1, 4)), (Knight, random.randint(1, 4))],
        }

        i = 0
        for piece, count in pieces['WHITE']:
            for a in range(count):
                self.add_piece(piece('WHITE'), cell_list[i])
                i+=1
                white_cnt+= 1

        for piece, count in pieces['BLACK']:
            for a in range(count):
                self.add_piece(piece('BLACK'), cell_list[i])
                i+=1
                black_cnt += 1
        return white_cnt, black_cnt


class Piece(ABC):
    def __init__(self, color, symbol):
        self._position = None
        self._color = color.strip().upper()
        self.symbol = symbol
        if self.get_color() not in ("WHITE", "BLACK"):
            raise ValueError("White/Black only")

    def get_color(self):
        return self._color

    def get_position(self):
        return self._position

    def _set_position(self, pos):
        self._position = pos

    @abstractmethod
    def available_moves(self, game):
        pass

class Empty():
    def available_moves(self, game):
        return []

EMPTY_CELL = Empty()

class King(Piece):
    def __init__(self, color):
        super().__init__(color, '♚' if color.strip().upper() == 'BLACK' else '♔')

    def available_moves(self, game):
        curr_pos = self.get_position()
        col_pos, row_pos = game._parse_position(curr_pos)

        moves = []
        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            flag = game._to_position(row_pos + x, col_pos + y)
            if not flag:
                continue

            cell = game.get_piece(flag)
            if cell is not EMPTY_CELL:
                if cell.get_color() == self.get_color():
                    continue

            moves.append(flag)

        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, '♛' if color.strip().upper() == 'BLACK' else '♕')

    def available_moves(self, game):
        curr_pos = self.get_position()
        col_pos, row_pos = game._parse_position(curr_pos)

        moves = []
        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            slide = 1

            while True:
                curr_row_pos = row_pos + x * slide
                curr_col_pos = col_pos + y * slide

                flag = game._to_position(curr_row_pos, curr_col_pos)
                if not flag:
                    break

                cell = game.get_piece(flag)
                if cell is not EMPTY_CELL:
                    if cell.get_color() != self.get_color():
                        moves.append(flag)
                    break

                moves.append(flag)
                slide += 1

        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, '♞' if color.strip().upper() == 'BLACK' else '♘')

    def available_moves(self, game):
        curr_pos = self.get_position()
        col_pos, row_pos = game._parse_position(curr_pos)

        moves = []
        possible_changes = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]

        for x, y in possible_changes:
            flag = game._to_position(row_pos + x, col_pos + y)
            if not flag:
                continue

            cell = game.get_piece(flag)
            if cell is not EMPTY_CELL:
                if cell.get_color() == self.get_color():
                    continue

            moves.append(flag)

        return moves

while True:
    key = input("Start a new game? Y/N").strip().upper()

    if key == "N" or key == "NO":
        print("Goodbye!")
        exit()

    elif key != "Y" and key != "YES":
        print("No such key! Use N/NO or Y/YES")
        continue

    D = GameEngine()
    white_cnt, black_cnt = D.distribute_pieces()
    while white_cnt > 0 and black_cnt > 0:
        D.display_board()
        print(f"""    White pieces: {white_cnt}
    Black pieces: {black_cnt}""")
        print(f'{D.get_state()}s turn')
        select_fr = input('Select a piece:').strip().upper()
        try:
            selected_piece = D.get_piece(select_fr)
        except ValueError:
            print('Outside of board!')
            continue
        if selected_piece is EMPTY_CELL:
            print('Empty cell, select a piece!')
            continue
        if selected_piece.get_color() != D.get_state():
            print(f"That's not your piece, you play as {D.get_state()}")
            continue
        print(selected_piece.available_moves(D))
        select_to = input('Select a cell to move to. If you changed mind type 0').strip().upper()
        try:
            if select_to == '0':
                continue
            if select_to not in selected_piece.available_moves(D):
                print('Invalid move!')
                continue
        except ValueError:
            print('Outside of board!')
            continue
        selected_piece = D.get_piece(select_to)
        if selected_piece is not EMPTY_CELL:
            if selected_piece.get_color() == 'WHITE':
                white_cnt -= 1
            else:
                black_cnt -= 1
        D.move(select_fr, select_to)
        if D.get_state() == 'WHITE':
            D.set_state('BLACK')
        else:
            D.set_state('WHITE')
        continue
    print(f'The winner is {'whites' if white_cnt > black_cnt else 'blacks'}')