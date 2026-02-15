from abc import ABC, abstractmethod

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
            return False
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

class Empty():
    def available_moves(self):
        return []

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.get_color() not in ("White", "Black"): raise ValueError("White/Black only")
        self.symbol = '♚' if self.get_color() == 'Black' else '♔'

    def available_moves(self, game):
        curr_pos = self.get_position()

        col_pos, row_pos = game._parse_position(curr_pos)

        moves = []

        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            flag = game._to_position(row_pos + x, col_pos + y)
            if not flag:
                continue

            if game.get_cell(flag) is not Empty:
                if game.get_cell(flag).get_color() == game.get_cell(curr_pos).get_color():
                    continue

            moves.append(flag)

        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.get_color() not in ("White", "Black"): raise ValueError("White/Black only")
        self.symbol = '♛' if self.get_color() == 'Black' else '♕'

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

                if game.get_cell(flag) is not Empty:
                    if game.get_cell(flag).get_color() != game.get_cell(curr_pos).get_color():
                        moves.append(flag)
                        break
                    break
                slide += 1
                moves.append(flag)

        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self.symbol = '♞' if self._color == 'Black' else '♘'

    def available_moves(self, game):
        curr_pos = self.get_position()

        col_pos, row_pos = game._parse_position(curr_pos)

        moves = []

        possible_changes = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]

        for x, y in possible_changes:
            flag = game._to_position(row_pos + x, col_pos + y)
            if not flag:
                continue

            if game.get_cell(flag) is not Empty:
                if game.get_cell(flag).get_color() == game.get_cell(curr_pos).get_color():
                    continue

            moves.append(flag)

        return moves


D= GameEngine()

D.display_board()

D.add_piece(Knight('White'), 'H6')

D.display_board()

D.add_piece(King('Black'), 'G8')

D.display_board()

D.move('H6', 'G4')

D.display_board()

D.move('G4', 'F2')

D.display_board()

D.add_piece(Queen('Black'), 'D5')

D.display_board()

print(D.get_cell('D5').available_moves(D))