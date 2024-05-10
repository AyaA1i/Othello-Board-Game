import copy

INF = 1000000000


def get_move():
    row = input("Enter row: ")
    col = input("Enter col: ")
    while not row.isnumeric() or not col.isnumeric():
        print("\nPlease enter a valid row and col numbers.")
        row = input("Enter row: ")
        col = input("Enter col: ")
    return int(row), int(col)


class Othello:
    def __init__(self):
        self.board = [['.'] * 8 for i in range(8)]
        self.board[3][4] = self.board[4][3] = 'B'  # 1 for black
        self.board[3][3] = self.board[4][4] = 'W'  # 2 for white
        self.current_player = 'B'

    def display_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()

    def is_valid_move(self, row, col):
        if self.board[row][col] != '.':
            return False

        opponent = 'W' if self.current_player == 'B' else 'B'
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            nx = row + dx[i]
            ny = col + dy[i]
            found_opponent = False
            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == opponent:
                found_opponent = True
                nx = nx + dx[i]
                ny = ny + dy[i]

            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == self.current_player and found_opponent:
                return True

        return False

    def play(self, row, col):
        self.board[row][col] = self.current_player
        self.flip_disks(row, col)
        self.current_player = 'B' if self.current_player == 'W' else 'W'

    def flip_disks(self, row, col):
        opponent = 'W' if self.current_player == 'B' else 'B'
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            nx = row + dx[i]
            ny = col + dy[i]
            found_opponent = False
            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == opponent:
                found_opponent = True
                nx = nx + dx[i]
                ny = ny + dy[i]

            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == self.current_player and found_opponent:
                nx = row + dx[i]
                ny = col + dy[i]
                while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == opponent:
                    self.board[nx][ny] = self.current_player
                    nx = nx + dx[i]
                    ny = ny + dy[i]

    def get_all_valid_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    moves.append([i, j])
        return moves

    def is_over(self):
        if len(self.get_all_valid_moves()) == 0:
            self.current_player = 'B' if self.current_player == 'W' else 'W'
            moves = self.get_all_valid_moves()
            self.current_player = 'B' if self.current_player == 'W' else 'W'
            if len(moves) == 0:
                return True
        return False

    def display_winner(self):
        black_count = 0
        white_count = 0

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'B':
                    black_count += 1
                if self.board[i][j] == 'W':
                    white_count += 1

        print(f"You: {white_count}, Computer: {black_count}")
        if black_count < white_count:
            print("Congrats, You Won!")
        elif black_count > white_count:
            print("You Lost!")
        else:
            print("It's a Tie!")

    def get_score(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count - white_count


def minimax_alpha_beta(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or state.is_over() or len(state.get_all_valid_moves()) == 0:
        return [state.get_score(), None]

    if maximizing_player:
        max_score = -INF
        best_move = None

        children = state.get_all_valid_moves()
        for child in children:
            new_state = copy.deepcopy(state)
            new_state.play(child[0], child[1])
            player_ans = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False)

            # ans[0] -> score, ans[1] -> move
            if player_ans[0] > max_score:
                max_score = player_ans[0]
                best_move = child

            alpha = max(alpha, player_ans[0])
            if beta <= alpha:
                break

        return max_score, best_move
    else:
        min_score = INF
        best_move = None

        children = state.get_all_valid_moves()
        for child in children:
            new_state = copy.deepcopy(state)
            new_state.play(child[0], child[1])
            player_ans = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True)

            # ans[0] -> score, ans[1] -> move
            if player_ans[0] < min_score:
                min_score = player_ans[0]
                best_move = child

            alpha = min(alpha, player_ans[0])
            if beta <= alpha:
                break

        return min_score, best_move


# ---------------------------------------------------------------------------------------------------------------------

print("Welcome to Othello Game!")
print("How challenging you want the game to be?")
print("Pick a number:")
print("1- Easy")
print("3- Medium")
print("5- Hard")

game = Othello()
level = int(input(">> "))

print("Let's Begin! (Computer is Black, You are white)")
game.display_board()

while not game.is_over():
    if game.current_player == 'W':
        valid_moves = game.get_all_valid_moves()
        if len(valid_moves) > 0:
            print("Valid Moves:", valid_moves)
            move = get_move()

            while [move[0], move[1]] not in valid_moves:
                print("\nInvalid Move")
                print("Valid Moves:", valid_moves)
                move = get_move()

            game.play(move[0], move[1])
        else:
            game.current_player = 'B'
            print("You can't make any move, so your turn is skipped.")
    else:
        ans = minimax_alpha_beta(game, level, -INF, INF, True)
        if ans[1] is not None:
            game.play(ans[1][0], ans[1][1])
        else:
            game.current_player = 'W'
            print("Computer can't make any move, so it's your turn now.")

    game.display_board()

game.display_winner()
