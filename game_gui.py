import copy
import PySimpleGUI as sg

INF = 1000000000


# Function to initialize the GUI board
def initialize_gui_board():
    return [['.' for _ in range(8)] for _ in range(8)]


def update_gui_board(window, board):
    for i in range(8):
        for j in range(8):
            color = 'light blue' if board[i][j] == '.' else ('white' if board[i][j] == 'W' else 'black')
            window[(i, j)].update(board[i][j], button_color=('black', color))


def get_move_from_gui(event):
    try:
        row, col = event
        return row, col
    except ValueError:
        return None


def create_gui_layout():
    layout = [[sg.Button('', size=(3, 1), key=(i, j), button_color='light blue') for j in range(8)] for i in range(8)]
    layout.append([sg.Button('Quit')])
    return layout


class Othello:
    def __init__(self):
        self.board = initialize_gui_board()
        self.board[3][4] = self.board[4][3] = 'B'
        self.board[3][3] = self.board[4][4] = 'W'
        self.current_player = 'W'

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
            if len(moves) == 0:
                return True
            self.current_player = 'B' if self.current_player == 'W' else 'W'
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

        sg.popup(f"You: {white_count}, Computer: {black_count}")
        if black_count < white_count:
            sg.popup("Congrats, You Won!")
        elif black_count > white_count:
            sg.popup("You Lost!")
        else:
            sg.popup("It's a Tie!")

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


def main():
    level = 0

    levels = ["Easy", "Medium", "Hard"]
    lst = sg.Combo(levels, font=('Arial Bold', 14), key='-COMBO-')
    layout = [[sg.Text("Pick a Level", font=('Arial Bold', 14)), lst, sg.Button('Ok'), sg.Button('Exit')]]
    level_window = sg.Window('Level', layout, size=(330, 100))
    while True:
        event, values = level_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Ok':
            value = values['-COMBO-']
            if value == 'Easy':
                level = 1
            elif value == 'Medium':
                level = 3
            else:
                level = 5
            break
    level_window.close()

    if level == 0:
        return

    game = Othello()
    layout = create_gui_layout()
    window = sg.Window('Othello', layout, finalize=True)
    update_gui_board(window, game.board)

    while True:
        if game.current_player == 'W':
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

            valid_moves = game.get_all_valid_moves()
            if len(valid_moves) > 0:
                move = get_move_from_gui(event)
                while [move[0], move[1]] not in valid_moves:
                    sg.popup("\nInvalid Move")
                    sg.popup("Valid Moves (0-based):", valid_moves)
                    event, values = window.read()
                    if event == sg.WINDOW_CLOSED or event == 'Quit':
                        break
                    move = get_move_from_gui(event)
                game.play(move[0], move[1])
                update_gui_board(window, game.board)
            else:
                game.current_player = 'B'
                sg.popup("You can't make any move, so your turn is skipped.")
        else:
            ans = minimax_alpha_beta(game, level, -INF, INF, True)
            if ans[1] is not None:
                game.play(ans[1][0], ans[1][1])
                update_gui_board(window, game.board)
            else:
                game.current_player = 'W'
                sg.popup("Computer can't make any move, so it's your turn now.")

        if game.is_over():
            game.display_winner()
            break

    window.close()


if __name__ == "__main__":
    main()
