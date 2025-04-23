import chess
import chess.engine
import torch
import numpy as np
from agents.double_agents import DoubleAgentsChess
from learnings.ppo import PPO
from chess import Chess
from chess import pieces as Pieces  # ✅ Fixes the warning


env = Chess(render_mode="rgb_array")
ppo_model = torch.load("results/DoubleAgents/white_ppo.pt")
agent = DoubleAgentsChess(
    env=env,
    learner=ppo_model,
    episodes=1,
    train_on=1,
    result_folder="results/",
)

engine = chess.engine.SimpleEngine.popen_uci("/Users/tejaswi/Desktop/stockfish")  # nid to change path to where UR stockfish is
# Stockfish is super good so we are nerfing it by giving a latency limit of 0.1
stockfish_time = 0.1 

def run_game(agent_is_white=True):
    env.reset()
    board = chess.Board()
    turn = chess.WHITE if agent_is_white else chess.BLACK

    while not board.is_game_over():
        if board.turn == turn:
            state = env.get_state(Pieces.WHITE if agent_is_white else Pieces.BLACK)
            _, mask = env.get_all_actions(Pieces.WHITE if agent_is_white else Pieces.BLACK)[-2:]
            action, _, _ = ppo_model.take_action(state, mask)
            source_pos, possible_moves, _ = env.get_all_actions(Pieces.WHITE if agent_is_white else Pieces.BLACK)
            move = chess.Move.from_uci(env_move_to_uci(source_pos[action], possible_moves[action]))
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move attempted. Agent forfeits.")
                return -1 if agent_is_white else 1
        else:
            result = engine.play(board, chess.engine.Limit(time=stockfish_time))
            board.push(result.move)

    result = board.result()
    if result == "1-0":
        return 1 if agent_is_white else -1
    elif result == "0-1":
        return -1 if agent_is_white else 1
    else:
        return 0
#KIV THIS
# Need to check if this part has any formatting error. Standardise based on our board.
def env_move_to_uci(src, dst):
    return f"{chr(dst[1] + 97)}{8 - dst[0]}{chr(src[1] + 97)}{8 - src[0]}"

num_games = 20
results = []
for i in range(num_games):
    print(f"Game {i+1}")
    agent_white = i % 2 == 0
    result = run_game(agent_white)
    results.append(result)

wins = results.count(1)
losses = results.count(-1)
draws = results.count(0)

print(f"Agent vs Stockfish over {num_games} games:")
print(f"Wins: {wins} | Losses: {losses} | Draws: {draws}")
print(f"Win rate: {wins / num_games:.2%}")
