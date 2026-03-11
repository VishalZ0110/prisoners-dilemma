# Prisoner's Dilemma — LLM Agent Simulation

A framework for studying emergent cooperation and defection strategies between two LLM agents playing a repeated Prisoner's Dilemma. The game rules are presented to each agent without naming the game, testing whether LLMs can discover cooperative equilibria on their own.

## Overview

Two agents — **Alpha** and **Beta** — each backed by a local LLM (via [Ollama](https://ollama.com)) play a configurable number of turns. On each turn, both agents independently choose to **COOPERATE** or **DEFECT** without seeing the other's current choice. After both decide, rewards are revealed, scores are updated, and the full history (from each agent's perspective) is fed into the next prompt.

### Payoff Matrix

| Alpha \ Beta | COOPERATE | DEFECT |
|---|---|---|
| **COOPERATE** | 3 , 3 | 0 , 5 |
| **DEFECT** | 5 , 0 | 1 , 1 |

## Project Structure

```
.
├── main.py          # Entry point — wires agents, state, and controller
├── config.py        # All hyperparameters and prompt templates
├── agent.py         # Agent class: prompt building, LLM call, response parsing
├── controller.py    # GameController: runs turns, logs results
├── game_state.py    # GameState & TurnRecord: scores, history, per-agent views
├── payoff.py        # Deterministic payoff matrix
└── skus.py          # SKU/category keyword list (sheet analysis utilities)
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally at `http://127.0.0.1:11434`
- A model pulled in Ollama (default: `qwen2:7b`)

Install Python dependencies:

```bash
python -m venv env_agents
source env_agents/bin/activate
pip install smolagents litellm
```

Pull the default model (if not already available):

```bash
ollama pull qwen2:7b
```

## Usage

```bash
python main.py
```

The simulation prints each turn's actions, reasoning, and running scores to stdout, then prints a final summary with cooperation statistics.

## Configuration

All hyperparameters live in `config.py`:

| Parameter | Default | Description |
|---|---|---|
| `N_TURNS` | `10` | Number of turns per game |
| `TEMPERATURE` | `0.9` | LLM sampling temperature |
| `API_BASE` | `http://127.0.0.1:11434` | Ollama API endpoint |
| `MODEL_ALPHA` | `ollama_chat/qwen2:7b` | Model for Agent Alpha |
| `MODEL_BETA` | `ollama_chat/qwen2:7b` | Model for Agent Beta |
| `AGENT_NAMES` | `["Agent Alpha", "Agent Beta"]` | Display names |
| `PROMPT_ALPHA` | — | Full prompt template for Alpha |
| `PROMPT_BETA` | — | Full prompt template for Beta |

Each agent can be given a **different model** and a **different prompt** (persona, strategy bias, additional instructions) independently.

### Using Different Models

```python
# config.py
MODEL_ALPHA = "ollama_chat/llama3:8b"
MODEL_BETA  = "ollama_chat/mistral:7b"
```

> **Note:** `keep_alive=0` is set on every LLM call so each model is evicted from GPU memory immediately after responding, preventing both models from competing for VRAM simultaneously.

## Example Output

```
──────────────────────────────────────────────────
  GAME START
──────────────────────────────────────────────────
  Agents  : Agent Alpha  vs  Agent Beta
  Turns   : 10

Turn 1
  Agent Alpha   : COOPERATE
  Reasoning     : Starting with cooperation to signal willingness for mutual gain.
  Agent Beta    : COOPERATE
  Reasoning     : Cooperating initially to establish trust.
  Score update  : Agent Alpha +3  |  Agent Beta +3
  Running totals: Agent Alpha 3   |  Agent Beta 3

...

──────────────────────────────────────────────────
  FINAL RESULTS
──────────────────────────────────────────────────
  Agent Alpha   : 28 points
  Agent Beta    : 28 points
  Score gap     : 0  (in favour of neither)

──────────────────────────────────────────────────
  COOPERATION STATS
──────────────────────────────────────────────────
  Agent Alpha   : 9 cooperations  /  1 defections  (90.0%)
  Agent Beta    : 9 cooperations  /  1 defections  (90.0%)
  Mutual cooperate : 8 turns
  Mutual defect    : 0 turns
```

## How It Works

1. **`main.py`** builds two `Agent` instances (each with its own `LiteLLMModel`) and a shared `GameState`, then hands them to `GameController.run()`.
2. **`GameController`** iterates for `N_TURNS`. Each turn it calls both agents in sequence (neither sees the other's current choice), computes payoffs, and records the result.
3. **`Agent.decide()`** formats the prompt template with the current game state, sends it to the LLM, and robustly parses the response — trying full JSON parse, then regex extraction, then plain-text keyword scan, falling back to DEFECT.
4. **`GameState`** maintains cumulative scores and renders history from each agent's first-person perspective (`You: COOPERATE / Agent Beta: DEFECT`).
