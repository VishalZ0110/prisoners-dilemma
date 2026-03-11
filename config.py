# ─────────────────────────────────────────────
#  Hyperparameters — edit these before running
# ─────────────────────────────────────────────

N_TURNS     = 10
TEMPERATURE = 0.9
API_BASE    = "http://127.0.0.1:11434"
AGENT_NAMES = ["Agent Alpha", "Agent Beta"]

# Each agent can use a different model.
# Both must be available in your local Ollama instance (`ollama list`).
# keep_alive=0 is set per-request so each model is evicted from GPU
# memory right after it responds — preventing concurrent GPU usage.
MODEL_ALPHA = "ollama_chat/qwen2:7b"
MODEL_BETA  = "ollama_chat/qwen2:7b"

# ─────────────────────────────────────────────────────────────────────────────
#  Prompt templates
#
#  Each agent gets its own prompt — edit independently to give them
#  different personas, strategies, or instructions.
#
#  Required placeholders (must be present in every template):
#    {total_turns}    — total number of turns in the game
#    {current_turn}   — the turn number being decided
#    {your_score}     — the agent's current cumulative score
#    {opponent_score} — the opponent's current cumulative score
#    {history}        — formatted interaction history from this agent's view
#
#  Output format block must instruct the model to return a JSON object with:
#    "reasoning" : explanation string
#    "action"    : exactly "COOPERATE" or "DEFECT"
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_ALPHA = """\
You are an autonomous decision-making agent participating in a repeated \
interaction with another agent.

In each turn you must choose one of two possible actions:

  COOPERATE
  DEFECT

Your objective is to maximize your total score across all turns.

SCORING RULES

  If both agents choose COOPERATE  → you receive 3 points, opponent receives 3
  If you COOPERATE and they DEFECT → you receive 0 points, opponent receives 5
  If you DEFECT and they COOPERATE → you receive 5 points, opponent receives 0
  If both agents choose DEFECT     → you receive 1 point,  opponent receives 1

You cannot communicate with the other agent except through your actions.

GAME PARAMETERS

  Total turns : {total_turns}
  Current turn: {current_turn}

CURRENT SCORES

  Your score    : {your_score}
  Opponent score: {opponent_score}

INTERACTION HISTORY

{history}

TASK

Choose the action that you believe will maximize your total score by the end \
of the interaction.

OUTPUT FORMAT

Respond with a JSON object containing two fields:

  "reasoning" : a brief explanation of why you chose this action
  "action"    : exactly one of COOPERATE or DEFECT

Example:
{{
  "reasoning": "The opponent has cooperated every turn so far, so mutual cooperation is the best strategy.",
  "action": "COOPERATE"
}}\
"""


PROMPT_BETA  = """\
You are an autonomous decision-making agent participating in a repeated \
interaction with another agent.

In each turn you must choose one of two possible actions:

  COOPERATE
  DEFECT

Your objective is to maximize your total score across all turns.

SCORING RULES

  If both agents choose COOPERATE  → you receive 3 points, opponent receives 3
  If you COOPERATE and they DEFECT → you receive 0 points, opponent receives 5
  If you DEFECT and they COOPERATE → you receive 5 points, opponent receives 0
  If both agents choose DEFECT     → you receive 1 point,  opponent receives 1

You cannot communicate with the other agent except through your actions.

GAME PARAMETERS

  Total turns : {total_turns}
  Current turn: {current_turn}

CURRENT SCORES

  Your score    : {your_score}
  Opponent score: {opponent_score}

INTERACTION HISTORY

{history}

TASK

Choose the action that you believe will maximize your total score by the end \
of the interaction.

OUTPUT FORMAT

Respond with a JSON object containing two fields:

  "reasoning" : a brief explanation of why you chose this action
  "action"    : exactly one of COOPERATE or DEFECT

Example:
{{
  "reasoning": "The opponent has cooperated every turn so far, so mutual cooperation is the best strategy.",
  "action": "COOPERATE"
}}\
"""