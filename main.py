"""
main.py — Entry point for the two-agent interaction simulation.

Run with:
    python main.py

All hyperparameters live in config.py.
"""

from smolagents import LiteLLMModel

from config     import N_TURNS, TEMPERATURE, MODEL_ALPHA, MODEL_BETA, API_BASE, AGENT_NAMES, PROMPT_ALPHA, PROMPT_BETA
from game_state import GameState
from agent      import Agent
from controller import GameController


def build_model(model_id: str) -> LiteLLMModel:
    """Initialise an Ollama-backed LLM for the given model ID."""
    return LiteLLMModel(
        model_id    = model_id,
        api_base    = API_BASE,
        temperature = TEMPERATURE,
        num_ctx     = 8192,
    )


def main() -> None:
    # ── Separate model instances per agent ────────────────────────────
    # Each agent gets its own LiteLLMModel so they can use different
    # underlying models. keep_alive=0 (set in Agent._call_llm) ensures
    # each model is evicted from GPU memory right after it responds.
    alpha_name, beta_name = AGENT_NAMES
    agent_alpha = Agent(name=alpha_name, opponent_name=beta_name,  model=build_model(MODEL_ALPHA), prompt_template=PROMPT_ALPHA)
    agent_beta  = Agent(name=beta_name,  opponent_name=alpha_name, model=build_model(MODEL_BETA),  prompt_template=PROMPT_BETA)

    # ── Game state ────────────────────────────────────────────────────
    state = GameState(total_turns=N_TURNS, agent_names=AGENT_NAMES)

    # ── Run ───────────────────────────────────────────────────────────
    controller = GameController(agent_alpha, agent_beta, state)
    controller.run()


if __name__ == "__main__":
    main()
