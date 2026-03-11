import json
import re

from smolagents import LiteLLMModel


class Agent:
    """
    Wraps a single LLM agent.

    Responsibilities:
      - Build the prompt for the current game state
      - Call the LLM via smolagents LiteLLMModel
      - Parse the raw text response into {"reasoning": str, "action": str}

    The prompt template is supplied at construction time from config.py,
    so each agent can have a completely different prompt.
    """

    def __init__(
        self,
        name:            str,
        opponent_name:   str,
        model:           LiteLLMModel,
        prompt_template: str,
    ):
        self.name            = name
        self.opponent_name   = opponent_name
        self.model           = model
        self.prompt_template = prompt_template

    # ── Public API ────────────────────────────────────────────────────

    def decide(
        self,
        current_turn:   int,
        total_turns:    int,
        your_score:     int,
        opponent_score: int,
        history:        str,
    ) -> dict:
        """
        Ask the LLM to pick an action and return a dict:
            {"reasoning": <str>, "action": "COOPERATE" | "DEFECT"}

        Falls back to action="DEFECT" with a note in reasoning if the model
        returns an unrecognisable response.
        """
        prompt   = self._build_prompt(current_turn, total_turns, your_score, opponent_score, history)
        response = self._call_llm(prompt)
        result   = self._parse_response(response)
        return result

    # ── Private helpers ───────────────────────────────────────────────

    def _build_prompt(
        self,
        current_turn:   int,
        total_turns:    int,
        your_score:     int,
        opponent_score: int,
        history:        str,
    ) -> str:
        return self.prompt_template.format(
            total_turns    = total_turns,
            current_turn   = current_turn,
            your_score     = your_score,
            opponent_score = opponent_score,
            history        = history,
        )

    def _call_llm(self, prompt: str) -> str:
        """
        Send the prompt to the model and return the raw text reply.

        keep_alive=0 tells Ollama to unload this model from GPU memory
        immediately after responding, so the next agent's model can load
        without both competing for the same GPU memory.
        """
        response = self.model.generate(
            messages=[
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            max_tokens = 200,
            keep_alive = 0,
        )
        # smolagents returns a ChatMessage; .content holds the text
        return response.content if hasattr(response, "content") else str(response)

    def _parse_response(self, raw: str) -> dict:
        """
        Parse the model's response into {"reasoning": str, "action": str}.

        Strategy:
          1. Try to parse the whole response as JSON.
          2. If that fails, search for a JSON object anywhere in the text.
          3. Validate that "action" is COOPERATE or DEFECT; fix if not.
          4. Fall back to action=DEFECT with an explanatory reasoning note.
        """
        # ── Attempt 1: parse full response as JSON ────────────────────
        try:
            data = json.loads(raw.strip())
            return self._validate_parsed(data)
        except json.JSONDecodeError:
            pass

        # ── Attempt 2: extract the first {...} block from the text ─────
        match = re.search(r"\{.*?\}", raw, flags=re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                return self._validate_parsed(data)
            except json.JSONDecodeError:
                pass

        # ── Attempt 3: scan plain text for a keyword ──────────────────
        upper = raw.strip().upper()
        if "COOPERATE" in upper:
            return {"reasoning": raw.strip(), "action": "COOPERATE"}
        if "DEFECT" in upper:
            return {"reasoning": raw.strip(), "action": "DEFECT"}

        # ── Fallback ──────────────────────────────────────────────────
        return {"reasoning": f"Could not parse model output: {raw!r}", "action": "DEFECT"}

    def _validate_parsed(self, data: dict) -> dict:
        """Ensure 'action' is valid; keep 'reasoning' as-is."""
        reasoning = str(data.get("reasoning", "")).strip()
        action    = str(data.get("action", "")).strip().upper()
        if action not in ("COOPERATE", "DEFECT"):
            action = "DEFECT"
        return {"reasoning": reasoning, "action": action}
