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
        row_pos = ord('8') - ord(pos[1]) + 1

        flag = self.is_inside_board(col_pos, row_pos)

        if not flag:
            raise ValueError('Outside of board')

        return col_pos, row_pos

    def add_piece(self, piece, pos): # must reject adding to an occupied square (raise an error).
        col_pos, row_pos = self.parse_position(pos)

        if self.board[row_pos][col_pos] != '.':
            raise ValueError('Cell is already occupied')

        self.board[row_pos][col_pos] = piece
        print('Success')

    def to_position(self, row, col):
        pass

    def is_inside_board(self, col_pos, row_pos):

        if not (1<=row_pos <=8 and 1<=col_pos <= 8):
            return False

        return True

    def get_piece(self, pos):
        col_pos, row_pos = self.parse_position(pos)

        cell = self.board[row_pos][col_pos]

        if cell == '.':
            print(f"Empty cell")
            return None

        print(f"The piece: {cell.symbol}")
        return cell

    def remove_piece(self, pos): # returns the removed piece or None if empty.
        col_pos, row_pos = self.parse_position(pos)

        cell = self.board[row_pos][col_pos]

        if cell == '.':
            self.board[row_pos][col_pos] = '.'
            print(f"Empy cell")
            return None

        self.board[row_pos][col_pos] = '.'
        print(f"Removed piece: {cell.symbol}")
        return cell

    def display_board(self):
        for col in range(0, 10):
            for row in range(0, 10):
                if type(self.board[col][row]) is not str:
                    print(self.board[col][row].symbol, end = ' ')
                    continue
                print(self.board[col][row], end = ' ')
            print()

class King():
    def __init__(self, color):
        self.color = color
        if self.color == 'Black':
            self.symbol = '♚'
            return
        self.symbol = '♔'

    def available_moves(self, game, pos):
        pass

class Queen():
    def __init__(self, color):
        self.color = color
        if self.color == 'Black':
            self.symbol = '♛'
            return
        self.symbol = '♕'

    def available_moves(self, game, pos):
        pass

class Knight():
    def __init__(self, color):
        self.color = color
        if self.color == 'Black':
            self.symbol = '♞'
            return
        self.symbol = '♘'

    def available_moves(self, game, pos):
        pass

D = Game()

D.add_piece(Knight('White'), 'B8')

D.add_piece(Queen('Black'), 'B7')
D.add_piece(Queen('White'), 'B6')
D.add_piece(Queen('Black'), 'B5')
D.add_piece(Queen('Black'), 'B4')
D.display_board()