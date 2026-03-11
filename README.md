# Prisoner's Dilemma — LLM Agent Simulation

Two LLM agents play a repeated Prisoner's Dilemma via [Ollama](https://ollama.com). The game rules are presented without naming the game, testing whether LLMs discover cooperative strategies on their own.

## Payoff Matrix

| Alpha \ Beta | COOPERATE | DEFECT |
|---|---|---|
| **COOPERATE** | 3 , 3 | 0 , 5 |
| **DEFECT** | 5 , 0 | 1 , 1 |

## Setup

```bash
python -m venv env_agents && source env_agents/bin/activate
pip install -r requirements.txt
ollama pull qwen2:7b
```

## Usage

```bash
python main.py
```

## Configuration

Edit `config.py` to change models, turns, temperature, and per-agent prompts.

| Parameter | Default |
|---|---|
| `N_TURNS` | `10` |
| `TEMPERATURE` | `0.9` |
| `MODEL_ALPHA` / `MODEL_BETA` | `ollama_chat/qwen2:7b` |
| `API_BASE` | `http://127.0.0.1:11434` |

Each agent can use a different model and prompt independently. `keep_alive=0` ensures models are evicted from GPU memory after each response to avoid VRAM contention.

## Project Structure

```
main.py        # Entry point
config.py      # Hyperparameters and prompt templates
agent.py       # LLM call and response parsing
controller.py  # Turn loop and logging
game_state.py  # Scores and per-agent history
payoff.py      # Payoff matrix
```
