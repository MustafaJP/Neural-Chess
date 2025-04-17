from chess import moves
MOVE = -1

CHECK_WIN = 10
CHECK_LOSE = -CHECK_WIN

CHECK_MATE_WIN = 100
CHECK_MATE_LOSE = -CHECK_MATE_WIN

center_zones_occupation = [
    # Most central and important squares
    ((4, 3), 5), ((4, 4), 5), ((3, 3), 5), ((3, 4), 5),

    # Secondary central squares (near center)
    ((5, 2), 4), ((4, 2), 4), ((3, 2), 4), ((2, 2), 4),
    ((5, 5), 4), ((4, 5), 4), ((3, 5), 4), ((2, 5), 4),
    ((5, 3), 4), ((5, 4), 4), ((2, 3), 4), ((2, 4), 4)
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

def king_safety(chess_object, turn): 
    pos = find_king(chess_object.board[turn])
    king_position = (7 - pos[0], 7 - pos[1])
    squares_near_king = []
    correct_range = [i for i in range(8)]
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (king_position[0] + i) in correct_range and (king_position[1] + j) in correct_range and i != 0 and j != 0:
                squares_near_king.append((king_position[0] + i, king_position[1] + j))
    danger_score = 0

    for i in range(8):
        for j in range(8):
            piece = chess_object.board[1 - turn][i][j]
            if piece == 0 : # There is no piece
                continue
            
            current_square = (i, j)
            possible_moves_for_piece = moves.PIECES[piece]
            possible_next_positions = [(i + m[0], j + m[1]) for m in possible_moves_for_piece if i + m[0] in correct_range and j + m[1] in correct_range]
            correct_possible_attacking_king_position = []
            for possible_move in possible_next_positions:
                if piece != 3: # Not a knight because it can jump
                    if chess_object.is_path_empty(current_square, possible_move, 1 - turn) and possible_move in attacking_pieces_near_king:
                        correct_possible_attacking_king_position.append(possible_move)
                    danger_score += len(correct_possible_attacking_king_position) * attacking_pieces_near_king[piece]
                elif possible_move in attacking_pieces_near_king:
                    danger_score += len(correct_possible_attacking_king_position) * attacking_pieces_near_king[piece]
    return danger_score