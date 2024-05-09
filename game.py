import copy


class OthelloGame:
    def __init__(self):
        self.board = [[0] * 8 for i in range(8)]
        self.board[3][4] = self.board[4][3] = 1  # 1 for black
        self.board[3][3] = self.board[4][4] = 2  # 2 for white
        self.current_player = 1
        self.game_over = False

    def display_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.board[i][j] == 0:
                    print(".", end=" ")
                elif self.board[i][j] == 1:
                    print("B", end=" ")
                else:
                    print("W", end=" ")
            print()

    def get_move(self):
        row = input("Enter row: ")
        col = input("Enter col: ")
        while not row.isnumeric() or not col.isnumeric():
            print("Please enter a valid row and col numbers.")
            row = input("Enter row: ")
            col = input("Enter col: ")
        return int(row), int(col)

    def is_valid_move(self, row, col):
        if self.board[row][col] != 0:
            return False

        opponent = 2 if self.current_player == 1 else 1
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

    def make_move(self, row, col):
        # if not self.is_valid_move(row, col):  # skip turn if no valid move
        #     return False

        self.board[row][col] = self.current_player
        self.flip_disks(row, col)
        self.current_player = 1 if self.current_player == 2 else 2
        # if not self.get_all_valid_moves():
        #     self.current_player = 1 if self.current_player == 2 else 2
        #     if not self.get_all_valid_moves():
        #         self.game_over = True

        # return True

    def flip_disks(self, row, col):
        opponent = 2 if self.current_player == 1 else 1
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
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    valid_moves.append([i, j])
        return valid_moves

    def is_game_over(self):
        return self.game_over

    def display_winner(self):
        black_count = 0
        white_count = 0

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    black_count += 1
                if self.board[i][j] == 2:
                    white_count += 1

        print(f"You: {white_count}, Computer: {black_count}")
        if black_count < white_count:
            print("Congrats, You Won!")
        elif black_count > white_count:
            print("You Lost!")
        else:
            print("It's a Tie!")

    def get_score(self, player):
        player_count = sum(row.count(player) for row in self.board)
        opponent_count = sum(row.count(1 if player == 2 else 2) for row in self.board)
        return player_count - opponent_count


class MinimaxAlphaBeta:
    def __init__(self, depth):
        self.max_depth = depth

    def evaluate(self, game, player):
        return game.get_score(player)

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_game_over():
            player = 1 if maximizing_player else 2
            return self.evaluate(game, player), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game.get_all_valid_moves():
                new_game = copy.deepcopy(game)
                new_game.make_move(*move)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in game.get_all_valid_moves():
                new_game = copy.deepcopy(game)
                new_game.make_move(*move)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def find_best_move(self, game):
        eval, best_move = self.minimax(game, self.max_depth, float('-inf'), float('inf'), True)
        return best_move


# ---------------------------------------------------------------------------------------------------------------------

print("Welcome to Othello Game!")
print("How challenging you want the game to be?")
print("Pick a number:")
print("1- Easy")
print("3- Medium")
print("5- Hard")

level = int(input(">> "))

print("Let's Begin! (Computer is Black, You are white)")
game = OthelloGame()
game.display_board()

algorithm = MinimaxAlphaBeta(depth=level)

while not game.is_game_over():
    if game.current_player == 2:
        valid_moves = game.get_all_valid_moves()
        print("Valid Moves:", valid_moves)
        move = game.get_move()
        while [move[0], move[1]] not in valid_moves:
            print("\nInvalid Move")
            print("Valid Moves:", valid_moves)
            move = game.get_move()
    else:
        move = algorithm.find_best_move(game)

    game.make_move(*move)
    game.display_board()

game.display_winner()
