from abc import ABC, abstractmethod

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

    def parse_position(self, pos):
        col_pos = ord(pos[0]) - ord('A') + 1
        row_pos = ord('8') - ord(pos[1]) + 1

        flag = self.is_inside_board(col_pos, row_pos)

        if not flag:
            raise ValueError('Outside of board')

        return col_pos, row_pos

    def add_piece(self, piece, pos):
        col_pos, row_pos = self.parse_position(pos)

        if self.board[row_pos][col_pos] != '.':
            raise ValueError('Cell is already occupied')

        self.board[row_pos][col_pos] = piece
        piece.position = pos
        print('Success')

    def to_position(self, row, col):
        flag = self.is_inside_board(row, col)

        if not flag:
            raise ValueError('Outside of board')
        return chr(col + 64) + str(9 - row)

    def is_inside_board(self, col_pos, row_pos):

        if not (1<=row_pos <=8 and 1<=col_pos <= 8):
            return False

        return True

    def get_piece(self, pos):
        col_pos, row_pos = self.parse_position(pos)

        if self.board[row_pos][col_pos] == '.':
            print(f"Empty cell")
            return Empty
        print(f"The piece: {self.board[row_pos][col_pos].symbol}")
        return self.board[row_pos][col_pos]

    def remove_piece(self, pos):
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
        for row in range(0, 10):
            for col in range(0, 10):
                if type(self.board[row][col]) is not str:
                    print(self.board[row][col].symbol, end = ' ')
                    continue
                print(self.board[row][col], end = '　')
            print()

    def move(self, fr, to):
        col_pos, row_pos = self.parse_position(fr)
        to_col_pos, to_row_pos = self.parse_position(to)

        if self.board[row_pos][col_pos] == '.':
            print('No piece on cell')
            return

        if to not in self.board[row_pos][col_pos].available_moves(self):
            print('Invalid move')
            return

        if self.board[to_row_pos][to_col_pos] != '.':
            self.remove_piece(to)
            self.board[row_pos][col_pos].position = to
            self.board[to_row_pos][to_col_pos] = self.board[row_pos][col_pos]

            self.board[row_pos][col_pos] = '.'
            return
        self.board[row_pos][col_pos].position = to
        self.board[to_row_pos][to_col_pos] = self.board[row_pos][col_pos]
        self.board[row_pos][col_pos] = '.'

class Empty():
    def available_moves(self):
        return []

class King():
    def __init__(self, color):
        self.position = None
        self.color = color
        if self.color == 'Black':
            self.symbol = '♚'
            return
        self.symbol = '♔'

    def available_moves(self, game):
        col_pos, row_pos = game.parse_position(self.position)

        moves = []

        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            flag = game.is_inside_board(row_pos + x, col_pos + y)
            if not flag:
                continue

            if game.board[row_pos + x][col_pos + y] != '.':
                if game.board[row_pos + x][col_pos + y].color == game.board[row_pos][col_pos].color:
                    continue

            moves.append(game.to_position(row_pos + x, col_pos + y))

        return moves


class Queen():
    def __init__(self, color):
        self.position = None
        self.color = color
        if self.color == 'Black':
            self.symbol = '♛'
            return
        self.symbol = '♕'

    def available_moves(self, game):
        col_pos, row_pos = game.parse_position(self.position)

        moves = []

        possible_changes = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]

        for x, y in possible_changes:
            slide = 1

            while True:
                curr_row_pos = row_pos + x * slide
                curr_col_pos = col_pos + y * slide

                flag = game.is_inside_board(curr_row_pos, curr_col_pos)
                if not flag:
                    break

                if game.board[curr_row_pos][curr_col_pos] != '.':
                    if game.board[curr_row_pos][curr_col_pos].color != game.board[row_pos][col_pos].color:
                        moves.append(game.to_position(curr_row_pos, curr_col_pos))
                        break
                    break
                slide += 1
                moves.append(game.to_position(curr_row_pos, curr_col_pos))

        return moves


class Knight():
    def __init__(self, color):
        self.position = None
        self.color = color
        if self.color == 'Black':
            self.symbol = '♞'
            return
        self.symbol = '♘'

    def available_moves(self, game):
        col_pos, row_pos = game.parse_position(self.position)

        moves = []

        possible_changes = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]

        for x, y in possible_changes:
            flag = game.is_inside_board(row_pos + x, col_pos + y)
            if not flag:
                continue

            if game.board[row_pos + x][col_pos + y] != '.':
                if game.board[row_pos + x][col_pos + y].color == game.board[row_pos][col_pos].color:
                    continue

            moves.append(game.to_position(row_pos + x, col_pos + y))

        return moves


D = Game()

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