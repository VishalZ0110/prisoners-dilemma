# Prisoner's Dilemma — LLM Agent Simulation

Two LLM agents play a repeated [Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) against each other, powered by local models via [Ollama](https://ollama.com). Each agent is given only the scoring rules and interaction history — the game is never named — to test whether LLMs can independently discover cooperative equilibria through repeated interaction.

On every turn, both agents simultaneously choose to **COOPERATE** or **DEFECT** without seeing the other's current decision. Choices are revealed together, rewards are applied, and each agent receives an updated history written from its own first-person perspective before the next turn. This mirrors the information structure of the classical game while keeping the prompt model-agnostic.

The two agents can run different underlying models and carry completely independent prompt templates, making it easy to pit different strategies, personas, or model sizes against each other.

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
