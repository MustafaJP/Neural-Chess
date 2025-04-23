import torch
import pygame
from chess import Chess
from learnings.ppo import PPO

# === Load environment and model ===
env = Chess(window_size=512, max_steps=128, render_mode="human")
env.reset()

# Get dimensions
input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n

# === Load trained model ===
ppo = torch.load("results/SingleAgent/single_agent_ppo.pt", map_location='cpu')
model = ppo.actor
model.eval()

# === Set human color ===
human_turn = 0  # 0 = White, 1 = Black

# === Game state ===
selected_square = None
running = True
done = False
human_turn = 0  # 0 = White, 1 = Black

# === Game loop ===
while running and not done:
    env.render()
    pygame.time.wait(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # === Human player's move ===
        if env.turn == human_turn and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // env.cell_size
            row = mouse_y // env.cell_size

            if selected_square is None:
                selected_square = (row, col)
            else:
                # Check if the clicked move is legal
                source_pos, possible_dests, action_mask = env.get_all_actions(env.turn)

                found_valid = False
                for i in range(len(action_mask)):
                    if (
                        action_mask[i]
                        and tuple(source_pos[i]) == selected_square
                        and tuple(possible_dests[i]) == (row, col)
                    ):
                        rewards, done, info = env.step(i)
                        selected_square = None
                        found_valid = True
                        break

                if not found_valid:
                    selected_square = None  # Reset if move was invalid

    # === AI Move ===
    if env.turn != human_turn and not done:
        state = env.get_state(env.turn)
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        _, _, action_mask = env.get_all_actions(env.turn)
        action_mask_tensor = torch.tensor(action_mask, dtype=torch.float32).unsqueeze(0)

        dist = model(state_tensor, action_mask_tensor)
        action = torch.argmax(dist.logits, dim=1).item()

        rewards, done, info = env.step(action)

# === Clean up ===
env.close()
pygame.quit()