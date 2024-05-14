import copy
import PySimpleGUI as sg

INF = 1000000000
white_disks = 30
black_disks = 30


def update_board(window, board):
    for i in range(8):
        for j in range(8):
            color = "light blue" if board[i][j] == "." else ("white" if board[i][j] == "W" else "black")
            window[(i, j)].update(board[i][j], button_color=("black", color))


def get_move_from_user(event):
    row, col = event
    return row, col


def create_layout():
    layout = [[sg.Button("", size=(3, 1), key=(i, j), button_color="light blue") for j in range(8)] for i in range(8)]
    layout.append([sg.Button("Quit")])
    return layout


def minimax_alpha_beta(game, depth, white_disk_count, black_disk_count, alpha, beta, maximizing_player):
    if (depth == 0 or game.is_over() or len(game.get_all_valid_moves()) == 0
            or (maximizing_player and white_disk_count == 0)
            or (not maximizing_player and black_disk_count == 0)):
        return [game.get_score(), None]

    if maximizing_player:
        max_score = -INF
        best_move = None

        children = game.get_all_valid_moves()
        for child in children:
            new_game = copy.deepcopy(game)
            new_game.play(child[0], child[1])
            player_ans = minimax_alpha_beta(new_game, depth - 1,
                                            white_disk_count - 1, black_disk_count, alpha, beta, False)

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

        children = game.get_all_valid_moves()
        for child in children:
            new_game = copy.deepcopy(game)
            new_game.play(child[0], child[1])
            player_ans = minimax_alpha_beta(new_game, depth - 1,
                                            white_disk_count, black_disk_count - 1, alpha, beta, True)

            # ans[0] -> score, ans[1] -> move
            if player_ans[0] < min_score:
                min_score = player_ans[0]
                best_move = child

            beta = min(beta, player_ans[0])
            if beta <= alpha:
                break

        return min_score, best_move


class Othello:
    def __init__(self):
        self.board = [["." for _ in range(8)] for _ in range(8)]
        self.board[3][4] = self.board[4][3] = "B"
        self.board[3][3] = self.board[4][4] = "W"
        self.current_player = "B"

    def is_valid_move(self, row, col):
        global black_disks, white_disks
        if (self.board[row][col] != "." or
                (self.current_player == "W" and white_disks == 0) or (self.current_player == "B" and black_disks == 0)):
            return False

        opponent = "W" if self.current_player == "B" else "B"
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
        self.outflank(row, col)
        self.current_player = "B" if self.current_player == "W" else "W"

    def outflank(self, row, col):
        opponent = "W" if self.current_player == "B" else "B"
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
        if white_disks == 0 and black_disks == 0:
            return True

        if len(self.get_all_valid_moves()) == 0:
            self.current_player = "B" if self.current_player == "W" else "W"
            moves = self.get_all_valid_moves()
            if len(moves) == 0:
                return True
            self.current_player = "B" if self.current_player == "W" else "W"
        return False

    def display_winner(self):
        black_count = 0
        white_count = 0

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "B":
                    black_count += 1
                if self.board[i][j] == "W":
                    white_count += 1

        sg.popup(f"You: {black_count}, Computer: {white_count}")
        if black_count > white_count:
            sg.popup("Congrats, You Won!")
        elif black_count < white_count:
            sg.popup("You Lost!")
        else:
            sg.popup("It's a Tie!")

    def get_score(self):
        black_count = sum(row.count("B") for row in self.board)
        white_count = sum(row.count("W") for row in self.board)
        return white_count - black_count


def initialize_game_gui():
    level = 0

    levels = ["Easy", "Medium", "Hard"]
    lst = sg.Combo(levels, font=("Arial Bold", 14), key="-COMBO-")
    layout = [[sg.Text("Pick a Level", font=("Arial Bold", 14)), lst, sg.Button("Ok"), sg.Button("Exit")]]
    level_window = sg.Window("Level", layout, size=(330, 100))
    while True:
        event, values = level_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Ok":
            value = values["-COMBO-"]
            if value == "Easy":
                level = 1
            elif value == "Medium":
                level = 3
            else:
                level = 5
            break
    level_window.close()

    return level


class GameController:
    global white_disks, black_disks
    def run(self):
        global black_disks, white_disks
        level = initialize_game_gui()
        if level == 0:
            return

        game = Othello()
        layout = create_layout()
        window = sg.Window("Othello", layout, finalize=True)
        update_board(window, game.board)

        while True:
            if game.is_over():
                game.display_winner()
                break

            if game.current_player == "B":
                if black_disks == 0:
                    game.current_player = "W"
                    sg.popup("You ran out of disks, so you can't make any move.")
                else:
                    valid_moves = game.get_all_valid_moves()
                    if len(valid_moves) > 0:
                        sg.popup("Valid Moves (0-based):", valid_moves)
                        event, values = window.read()
                        if event == sg.WINDOW_CLOSED or event == "Quit":
                            break
                        move = get_move_from_user(event)
                        while [move[0], move[1]] not in valid_moves:
                            sg.popup("\nInvalid Move")
                            sg.popup("Valid Moves (0-based):", valid_moves)
                            event, values = window.read()
                            if event == sg.WINDOW_CLOSED or event == "Quit":
                                break
                            move = get_move_from_user(event)
                        game.play(move[0], move[1])
                        update_board(window, game.board)
                        black_disks -= 1
                    else:
                        game.current_player = "W"
                        sg.popup("You can't make any move, so your turn is skipped.")
            else:
                if white_disks == 0:
                    game.current_player = "B"
                    sg.popup("Computer ran out of disks, so it's your turn now.")
                else:
                    ans = minimax_alpha_beta(game, level, white_disks, black_disks, -INF, INF, True)
                    if ans[1] is not None:
                        game.play(ans[1][0], ans[1][1])
                        update_board(window, game.board)
                        white_disks -= 1
                    else:
                        game.current_player = "B"
                        sg.popup("Computer can't make any move, so it's your turn now.")

        window.close()


if __name__ == "__main__":
    controller = GameController()
    controller.run()
