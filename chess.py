from abc import ABC, abstractmethod

class GameEngine():

    # Private:

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

    def _parse_position(self, pos):
        col_pos = ord(pos[0]) - ord('A') + 1
        row_pos = ord('8') - ord(pos[1]) + 1

        flag = self._is_inside_board(col_pos, row_pos)

        if not flag:
            raise ValueError('Outside of board')

        return col_pos, row_pos

    def _to_position(self, row, col):
        flag = self._is_inside_board(row, col)

        if not flag:
            raise ValueError('Outside of board')
        return chr(col + 64) + str(9 - row)

    def _is_inside_board(self, col_pos, row_pos):
        if not (1<=row_pos <=8 and 1<=col_pos <= 8):
            return False

        return True

    def _val_move(self, fr, to):
        col_pos, row_pos = self._parse_position(fr)
        to_col_pos, to_row_pos = self._parse_position(to)

        if self.get_cell(to) is not Empty:
            self.remove_piece(to)

        self.get_cell(fr)._set_position(to)
        self._set_cell(self.get_cell(fr), to)
        self._set_cell('.', fr)

    def _set_cell(self, piece, pos):
        col_pos, row_pos = self._parse_position(pos)

        self._board[row_pos][col_pos] = piece
        if type(piece) is not str: piece._set_position(pos)

    # Public:

    def add_piece(self, piece, pos):
        if self.get_cell(pos) is not Empty:
            raise ValueError('Cell is already occupied')

        self._set_cell(piece, pos)
        print('Success')

    def remove_piece(self, pos):
        piece = self.get_cell(pos)

        if piece is Empty:
            print(f"Empy cell")
            return None

        self._set_cell('.', pos)
        print(f"Removed piece: {piece.symbol}")

    def get_cell(self, pos):
        col_pos, row_pos = self._parse_position(pos)

        if self._board[row_pos][col_pos] == '.':
            return Empty

        return self._board[row_pos][col_pos]

    def display_board(self):
        for row in range(0, 10):
            for col in range(0, 10):
                if type(self._board[row][col]) is not str:
                    print(self._board[row][col].symbol, end = ' ')
                    continue
                print(self._board[row][col], end = '　')
            print()

    def move(self, fr, to):

        if self.get_cell(fr) is Empty:
            return

        if to not in self.get_cell(fr).available_moves(self):
            return

        self._val_move(fr, to)

class Piece(ABC):
    def __init__(self, color):
        self._position = None
        self._color = color

    def get_color(self):
        return self._color

    def get_position(self):
        return self._position

    def _set_position(self, pos):
        self._position = pos

    @abstractmethod
    def available_moves(self): # Returns list of available moves
        pass

class Empty(Piece):
    def available_moves(self):
        return []

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self.symbol = '♚' if self._color == 'Black' else '♔'

    def available_moves(self, game):
        col_pos, row_pos = game._parse_position(self._position)

        moves = []

        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            flag = game._is_inside_board(row_pos + x, col_pos + y)
            if not flag:
                continue

            if game._board[row_pos + x][col_pos + y] != '.':
                if game._board[row_pos + x][col_pos + y]._color == game._board[row_pos][col_pos]._color:
                    continue

            moves.append(game._to_position(row_pos + x, col_pos + y))

        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self.symbol = '♛' if self._color == 'Black' else '♕'

    def available_moves(self, game):
        col_pos, row_pos = game._parse_position(self._position)

        moves = []

        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            slide = 1

            while True:
                curr_row_pos = row_pos + x * slide
                curr_col_pos = col_pos + y * slide

                flag = game._is_inside_board(curr_row_pos, curr_col_pos)
                if not flag:
                    break

                if game._board[curr_row_pos][curr_col_pos] != '.':
                    if game._board[curr_row_pos][curr_col_pos]._color != game._board[row_pos][col_pos]._color:
                        moves.append(game._to_position(curr_row_pos, curr_col_pos))
                        break
                    break
                slide += 1
                moves.append(game._to_position(curr_row_pos, curr_col_pos))

        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self.symbol = '♞' if self._color == 'Black' else '♘'

    def available_moves(self, game):
        col_pos, row_pos = game._parse_position(self._position)

        moves = []

        possible_changes = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]

        for x, y in possible_changes:
            flag = game._is_inside_board(row_pos + x, col_pos + y)
            if not flag:
                continue

            if game._board[row_pos + x][col_pos + y] != '.':
                if game._board[row_pos + x][col_pos + y]._color == game._board[row_pos][col_pos]._color:
                    continue

            moves.append(game._to_position(row_pos + x, col_pos + y))

        return moves


D = GameEngine()

D.add_piece(Knight('White'), 'D6')

D.add_piece(King('Black'), 'B7')

D.add_piece(Queen('Black'), 'B4')

D.add_piece(King('Black'), 'D1')

some_piece = D.get_cell('A1')

print(some_piece.available_moves(D))

D.move('B4', 'D6')

D.display_board()

D.move('D6', 'D1')

D.move('D1', 'D2')
D.move('D2', 'D3')

D.add_piece(Knight('White'), 'F7')

D.move('F7', 'D6')

D.move('D6', 'B7')

D.display_board()

a = D.get_cell('B7')

print(a.available_moves(D))