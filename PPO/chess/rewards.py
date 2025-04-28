import numpy as np
from chess import moves
from chess.pieces import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

MOVE = -1

CHECK_WIN = 10
CHECK_LOSE = -CHECK_WIN

CHECK_MATE_WIN = 100
CHECK_MATE_LOSE = -CHECK_MATE_WIN

CAPTURE_REWARDS = {
    PAWN: 1,
    KNIGHT: 3,
    BISHOP: 3,
    ROOK: 5,
    QUEEN: 9,
    KING: 100 
}

center_zones_occupation = [
    # Most central and important squares
    ((4, 3), 3), ((4, 4), 3), ((3, 3), 3), ((3, 4), 3),

    # Secondary central squares (near center)
    ((5, 2), 2), ((4, 2), 2), ((3, 2), 2), ((2, 2), 2),
    ((5, 5), 2), ((4, 5), 2), ((3, 5), 2), ((2, 5), 2),
    ((5, 3), 2), ((5, 4), 2), ((2, 3), 2), ((2, 4), 2)
]

attacking_pieces_near_king = {
    1: 0.2,
    2: 0.3,
    3: 0.5,
    4: 0.5,
    5: 1.0,
    6: 0.2
}

def central_control(new_pos):
    new_pos = tuple(new_pos)
    for position, reward in center_zones_occupation:
        if new_pos == position:
            return reward
    return 0

def find_king(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == 6:
                return (i, j)

def new_is_path_empty(board, from_pos, to_pos, turn):
    complete_board = board[1 - turn] + board[turn][::-1]
    from_row, from_col = from_pos
    to_row, to_col = to_pos

    delta_row = to_row - from_row
    delta_col = to_col - from_col

    # Determine direction of movement
    step_row = (delta_row > 0) - (delta_row < 0)
    step_col = (delta_col > 0) - (delta_col < 0)

    current_row = from_row + step_row
    current_col = from_col + step_col

    while (current_row, current_col) != (to_row, to_col):
        if complete_board[current_row][current_col] != 0:
            return False
        current_row += step_row
        current_col += step_col
    if board[turn][current_row][current_col] != 0:
        return False
    return True

def king_safety(chess_object, turn): 
    king_position = find_king(chess_object.board[turn])
    squares_near_king = []
    correct_range = [i for i in range(8)]

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i != 0 or j != 0) and (king_position[0] + i) in correct_range and (king_position[1] + j) in correct_range:
                squares_near_king.append((7 - king_position[0] + i, king_position[1] + j))
    danger_score = 0

    for i in range(8):
        for j in range(8):
            piece = chess_object.board[1 - turn][i][j]
            if piece == 0:
                continue

            current_square = (i, j)
            possible_moves_for_piece = moves.PIECES[piece]
            possible_next_positions = [(i + m[0], j + m[1]) for m in possible_moves_for_piece
                                       if i + m[0] in correct_range and j + m[1] in correct_range]

            attacking_moves = []

            for move in possible_next_positions:
                if move not in squares_near_king:
                    continue
                if piece != 3:  # Not a knight
                    if new_is_path_empty(chess_object.board, current_square, move, turn):
                        attacking_moves.append(move)
                else:  # Knight can jump
                    attacking_moves.append(move)
            score_contribution = len(attacking_moves) * attacking_pieces_near_king[piece]
            danger_score += score_contribution
    return danger_score
