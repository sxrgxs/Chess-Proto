class Game():

    def __init__(self):
        self.board = [
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

    def parse_position(self, pos): # must validate that pos is within A1-H8 and raise an error for invalid inputs.
        col_pos = ord(pos[0]) - ord('A') + 1
        row_pos = ord(pos[1]) + 1
        if not (1<=row_pos <=8 and 1<=col_pos <= 8):
            print('Invalid input')
            return
        return col_pos, row_pos

    def add_piece(self, piece, pos): # must reject adding to an occupied square (raise an error).
        pos.parse_position()
        if self.board[parsed_pos[0]][parsed_pos[1]] != '.':
            print('Space is already occupied')
            return
        self.board[parsed_pos[0]][parsed_pos[1]] = piece

    def to_position(self, row, col):
        pass

    def is_inside_board(self, pos):
        pass

    def get_piece(self, pos):
        pass

    def remove_piece(self, pos): # returns the removed piece or None if empty.
        pass

    def display_board(self):
        for row in self.board:
            print(' '.join(row))

class King():
    symbol = 'Ki'

    def __init__ (self, color):
        self.color = color

    def available_moves(self, game : 'Game', pos : str): # The method must return destination squares in chess notation
        # A destination square is allowed if it is on the board and is empty, OR it contains an opponent piece (capture).
        # A destination square is NOT allowed if it contains a piece of the same color.
        # King: 1 square in any direction (8 neighbors). Ignore castling and “moving into check”.
        pass

class Queen():
    symbol = 'Qu'

    def __init__ (self, color):
        self.color = color

    def available_moves(self, game : 'Game', pos : str): # The method must return destination squares in chess notation
        # A destination square is allowed if it is on the board and is empty, OR it contains an opponent piece (capture).
        # A destination square is NOT allowed if it contains a piece of the same color.
        # Queen: moves any number of squares horizontally, vertically, or diagonally until blocked
        pass

class Knight():
    symbol = 'Kn'

    def __init__(self, color):
        self.color = color
        if self.color == 'Black':
            Knight.symbol = '♚'
            return
        self.color = '♔'

    # A destination square is allowed if it is on the board and is empty, OR it contains an opponent piece (capture).
    # A destination square is NOT allowed if it contains a piece of the same color.
    # Knight: L-shape moves (±2, ±1). Knight can jump over pieces (blockers do not matter).

D = Game()

D.add_piece(Knight, 'E5')

D.display_board()