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

def central_control(new_pos):
    new_pos = tuple(new_pos)
    for position, reward in center_zones_occupation:
        if new_pos == position:
            return reward
    return 0