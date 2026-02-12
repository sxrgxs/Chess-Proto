from abc import ABC, abstractmethod

class Game(ABC):
    @abstractmethod
    def add_piece(self, piece, pos): # Adds piece on the chosen pos e.g. 'A1'
        pass
    @abstractmethod
    def remove_piece(self, pos): # Removes piece on the chosen pos e.g. 'A1'
        pass
    @abstractmethod
    def get_piece(self, pos): # Returns object of piece or None
        pass
    @abstractmethod
    def display_board(self): # Prints board
        pass
    @abstractmethod
    def move(self, fr, to): #moves piece from .. to ..
        pass

class GameEngine(Game):

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

    def add_piece(self, piece, pos):
        col_pos, row_pos = self._parse_position(pos)

        if self._board[row_pos][col_pos] != '.':
            raise ValueError('Cell is already occupied')

        self._board[row_pos][col_pos] = piece
        piece._position = pos
        print('Success')

    def to_position(self, row, col):
        flag = self._is_inside_board(row, col)

        if not flag:
            raise ValueError('Outside of board')
        return chr(col + 64) + str(9 - row)

    def _is_inside_board(self, col_pos, row_pos):

        if not (1<=row_pos <=8 and 1<=col_pos <= 8):
            return False

        return True

    def get_piece(self, pos):
        col_pos, row_pos = self._parse_position(pos)

        if self._board[row_pos][col_pos] == '.':
            print(f"Empty cell")
            return Empty
        print(f"The piece: {self._board[row_pos][col_pos]._symbol}")
        return self._board[row_pos][col_pos]

    def remove_piece(self, pos):
        col_pos, row_pos = self._parse_position(pos)

        cell = self._board[row_pos][col_pos]

        if cell == '.':
            self._board[row_pos][col_pos] = '.'
            print(f"Empy cell")
            return None

        self._board[row_pos][col_pos] = '.'
        print(f"Removed piece: {cell._symbol}")
        return cell

    def display_board(self):
        for row in range(0, 10):
            for col in range(0, 10):
                if type(self._board[row][col]) is not str:
                    print(self._board[row][col]._symbol, end = ' ')
                    continue
                print(self._board[row][col], end = '　')
            print()

    def move(self, fr, to):
        col_pos, row_pos = self._parse_position(fr)
        to_col_pos, to_row_pos = self._parse_position(to)

        if self._board[row_pos][col_pos] == '.':
            print('No piece on cell')
            return

        if to not in self._board[row_pos][col_pos].available_moves(self):
            print('Invalid move')
            return

        if self._board[to_row_pos][to_col_pos] != '.':
            self.remove_piece(to)
            self._board[row_pos][col_pos]._position = to
            self._board[to_row_pos][to_col_pos] = self._board[row_pos][col_pos]
            self._board[row_pos][col_pos] = '.'
            return
        self._board[row_pos][col_pos]._position = to
        self._board[to_row_pos][to_col_pos] = self._board[row_pos][col_pos]
        self._board[row_pos][col_pos] = '.'

class piece(ABC):
    def __init__(self, color):
        self._position = None
        self._color = color

    @abstractmethod
    def available_moves(self): # Returns list of available moves
        pass

class Empty(piece):
    def available_moves(self):
        return []

class King(piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self._symbol = '♚' if self._color == 'Black' else '♔'

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

            moves.append(game.to_position(row_pos + x, col_pos + y))

        return moves


class Queen(piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self._symbol = '♛' if self._color == 'Black' else '♕'

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
                        moves.append(game.to_position(curr_row_pos, curr_col_pos))
                        break
                    break
                slide += 1
                moves.append(game.to_position(curr_row_pos, curr_col_pos))

        return moves


class Knight(piece):
    def __init__(self, color):
        super().__init__(color)
        if self._color not in ("White", "Black"): raise ValueError("White/Black only")
        self._symbol = '♞' if self._color == 'Black' else '♘'

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

            moves.append(game.to_position(row_pos + x, col_pos + y))

        return moves


D = GameEngine()

D.add_piece(Knight('White'), 'D6')

D.add_piece(King('Black'), 'B7')

D.add_piece(Queen('Black'), 'B4')

D.add_piece(King('Black'), 'D1')

some_piece = D.get_piece('A1')

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

a = D.get_piece('B7')
print(a.available_moves(D))