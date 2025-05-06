import pygame
import chess
import torch
from chess import Chess
from chess import pieces as Pieces
from torch.serialization import add_safe_globals
from learnings.ppo import PPO
from learnings.ppo.actor import Actor

add_safe_globals([PPO])
add_safe_globals([Actor])
model = torch.load("PPO/results/DoubleAgents/white_ppo.pt", weights_only=False)
HUMAN_IS_WHITE = False
env = Chess(render_mode="human")
pygame.init()

def state_to_tensor(state):
    return torch.Tensor(state).unsqueeze(0).to(model.device)

def mask_to_tensor(mask):
    return torch.Tensor(mask).unsqueeze(0).to(model.device)

def get_agent_move(turn):
    state = env.get_state(turn)
    _, _, mask = env.get_all_actions(turn)
    action, _, _ = model.take_action(state, mask)
    src, dst = env.get_all_actions(turn)[0][action], env.get_all_actions(turn)[1][action]
    return tuple(src), tuple(dst)

def pos_to_coord(x, y, cell_size):
    if HUMAN_IS_WHITE:
        x = 7-x
        # y = 7-y
    return y * cell_size, x * cell_size

def coord_to_pos(mx, my, cell_size):
    row = my // cell_size
    col = mx // cell_size
    if HUMAN_IS_WHITE:
        row = 7 - row
        # col = 7 - col
    return row, col

def play_game():
    env.reset()
    running = True
    selected_pos = None
    cell_size = env.cell_size
    screen = env.screen

    while running and not env.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ((env.turn == Pieces.WHITE and HUMAN_IS_WHITE) or (env.turn == Pieces.BLACK and not HUMAN_IS_WHITE)):
                mx, my = pygame.mouse.get_pos()
                row, col = coord_to_pos(mx, my, cell_size)
                print(row,col)
                if selected_pos is None:
                    selected_pos = (row, col)
                else:
                    source = selected_pos
                    dest = (row, col)
                    try:
                        # Validate move
                        all_src, all_dst, all_mask = env.get_all_actions(env.turn)
                        for i in range(len(all_src)):
                            if tuple(all_src[i]) == source and tuple(all_dst[i]) == dest and all_mask[i]:
                                env.move_piece(source, dest, env.turn)
                                env.update_checks()
                                env.update_check_mates()
                                env.turn = 1 - env.turn
                                env.steps += 1
                                break
                        selected_pos = None
                    except:
                        print("Invalid move")
                        selected_pos = None

        if not env.done and ((env.turn == Pieces.WHITE and not HUMAN_IS_WHITE) or (env.turn == Pieces.BLACK and HUMAN_IS_WHITE)):
            src, dst = get_agent_move(env.turn)
            env.move_piece(src, dst, env.turn)
            env.update_checks()
            env.update_check_mates()
            env.turn = 1 - env.turn
            env.steps += 1

        env.render()

    pygame.quit()
    print("Game over!")

if __name__ == "__main__":
    play_game()
