# NeuralChess 🧠♟️

A reinforcement learning-based chess engine built on top of multi-agent deep RL techniques, with a strong focus on **custom reward shaping** to improve strategic gameplay.

## 🧩 Overview

NeuralChess is a modified and extended version of the open-source [Simple-MADRL-Chess](https://github.com/mhyrzt/Simple-MADRL-Chess) repository. While we adopt most of its architecture, our main contributions lie in **enhancing the reward function** to better reflect in-game strategies, and implementing several other improvements for **more balanced and intelligent gameplay**.

## 🚀 Motivation

Chess is a deterministic, perfect-information game, making it an ideal environment to experiment with reinforcement learning. Most traditional RL chess agents only reward final outcomes (+1/-1/0), overlooking strategic intermediate moves. This slows convergence and can lead to shallow play.

NeuralChess introduces nuanced, **multi-component reward signals** that help the model understand and evaluate:

- **Center control**
- **King safety (defense & attack)**
- **Material gain/loss**

## ⚙️ Key Features

- ✅ **Center Control Rewards** — Encourage piece placement in central and semi-central squares.
- ✅ **King Zone Evaluation** — Reward/penalize based on attack proximity to the enemy king or exposure around own king.
- ✅ **Material Tradeoffs** — Positive rewards for capturing pieces and penalties for losses, scaled by piece value.
- ✅ **Compatible with Stockfish** — Includes code for benchmarking model performance against [Stockfish](https://stockfishchess.org/).

## 📊 Results Summary

Compared to the baseline MADRL Chess:

- Rewards improved from ~-200 to ~-100 per game.
- Checkmate rates were more consistent across training.
- Black and white performances became more balanced.
- Number of moves remained similar, indicating no overfitting to shorter/longer games.

## 🔁 Based On

This project was built using:
- [Simple-MADRL-Chess](https://github.com/mhyrzt/Simple-MADRL-Chess) (base framework and architecture)
  
We thank the original authors for their excellent open-source implementation.

## 🛠️ Installation & Setup

```bash
git clone https://github.com/YOUR_USERNAME/NeuralChess.git
cd NeuralChess
pip install -r requirements.txt
```

Ensure [Stockfish](https://stockfishchess.org/download/) is installed and properly linked in your configuration.

## ▶️ How to Train

```bash
python train_agents.py
```

## ♟️ Play Against the Agent (Human vs Model)

```bash
python play_human_game.py
```

## 📈 Benchmarking vs Stockfish

```bash
python benchmark_vs_stockfish.py
```

## 📚 Report

For full details on methodology and experimental results, refer to the [NeuralChess Report (PDF)](./NeuralChess.pdf).

## 📌 Future Work

- Dynamic reward shaping based on game phase (opening, middlegame, endgame)
- Incorporating positional evaluation metrics like piece mobility and king tropism
- Adding visualization tools for training progress

## 📄 License

MIT License.
