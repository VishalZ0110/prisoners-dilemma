from agent      import Agent
from game_state import GameState
from payoff     import compute_payoff


class GameController:
    """
    Runs the game turn by turn.

    Each turn:
      1. Ask Agent Alpha for its action  (Alpha cannot see Beta's choice yet)
      2. Ask Agent Beta  for its action  (Beta  cannot see Alpha's choice yet)
      3. Reveal both choices, compute rewards, update state
      4. Log the result
    """

    def __init__(self, agent_alpha: Agent, agent_beta: Agent, state: GameState):
        self.agent_alpha = agent_alpha
        self.agent_beta  = agent_beta
        self.state       = state

    # ── Main loop ─────────────────────────────────────────────────────

    def run(self) -> None:
        print(self._header("GAME START"))
        print(f"  Agents  : {self.state.alpha_name}  vs  {self.state.beta_name}")
        print(f"  Turns   : {self.state.total_turns}")
        print()

        for _ in range(self.state.total_turns):
            self._run_one_turn()

        self._print_final_results()

    # ── Turn execution ────────────────────────────────────────────────

    def _run_one_turn(self) -> None:
        turn = self.state.current_turn

        # Each agent decides without seeing the opponent's choice for this turn
        result_alpha = self.agent_alpha.decide(
            current_turn   = turn,
            total_turns    = self.state.total_turns,
            your_score     = self.state.score_alpha,
            opponent_score = self.state.score_beta,
            history        = self.state.history_for_alpha(),
        )
        result_beta = self.agent_beta.decide(
            current_turn   = turn,
            total_turns    = self.state.total_turns,
            your_score     = self.state.score_beta,
            opponent_score = self.state.score_alpha,
            history        = self.state.history_for_beta(),
        )

        action_alpha    = result_alpha["action"]
        action_beta     = result_beta["action"]
        reasoning_alpha = result_alpha["reasoning"]
        reasoning_beta  = result_beta["reasoning"]

        reward_alpha, reward_beta = compute_payoff(action_alpha, action_beta)

        self.state.record_turn(
            action_alpha    = action_alpha,
            action_beta     = action_beta,
            reward_alpha    = reward_alpha,
            reward_beta     = reward_beta,
            reasoning_alpha = reasoning_alpha,
            reasoning_beta  = reasoning_beta,
        )

        self._log_turn(turn, action_alpha, action_beta, reward_alpha, reward_beta, reasoning_alpha, reasoning_beta)

    # ── Logging ───────────────────────────────────────────────────────

    def _log_turn(
        self,
        turn:             int,
        action_alpha:     str,
        action_beta:      str,
        reward_alpha:     int,
        reward_beta:      int,
        reasoning_alpha:  str,
        reasoning_beta:   str,
    ) -> None:
        alpha = self.state.alpha_name
        beta  = self.state.beta_name

        print(f"Turn {turn}")
        print(f"  {alpha:<14}: {action_alpha}")
        print(f"  Reasoning      : {reasoning_alpha}")
        print(f"  {beta:<14}: {action_beta}")
        print(f"  Reasoning      : {reasoning_beta}")
        print(f"  Score update   : {alpha} +{reward_alpha}  |  {beta} +{reward_beta}")
        print(f"  Running totals : {alpha} {self.state.score_alpha}  |  {beta} {self.state.score_beta}")
        print()

    # ── Final results ─────────────────────────────────────────────────

    def _print_final_results(self) -> None:
        history = self.state.history
        alpha   = self.state.alpha_name
        beta    = self.state.beta_name

        total_turns       = len(history)
        alpha_cooperates  = sum(1 for r in history if r.action_alpha == "COOPERATE")
        beta_cooperates   = sum(1 for r in history if r.action_beta  == "COOPERATE")
        alpha_defects     = total_turns - alpha_cooperates
        beta_defects      = total_turns - beta_cooperates
        mutual_cooperate  = sum(1 for r in history if r.action_alpha == "COOPERATE" and r.action_beta == "COOPERATE")
        mutual_defect     = sum(1 for r in history if r.action_alpha == "DEFECT"    and r.action_beta == "DEFECT")
        alpha_coop_rate   = alpha_cooperates / total_turns * 100
        beta_coop_rate    = beta_cooperates  / total_turns * 100

        print(self._header("FINAL RESULTS"))
        print(f"  {alpha:<14}: {self.state.score_alpha} points")
        print(f"  {beta:<14}: {self.state.score_beta} points")
        print(f"  Score gap      : {abs(self.state.score_alpha - self.state.score_beta)}"
              f"  (in favour of {'neither' if self.state.score_alpha == self.state.score_beta else (alpha if self.state.score_alpha > self.state.score_beta else beta)})")
        print()
        print(self._header("COOPERATION STATS"))
        print(f"  {alpha:<14}: {alpha_cooperates} cooperations  /  {alpha_defects} defections  ({alpha_coop_rate:.1f}%)")
        print(f"  {beta:<14}: {beta_cooperates}  cooperations  /  {beta_defects}  defections  ({beta_coop_rate:.1f}%)")
        print(f"  Mutual cooperate : {mutual_cooperate} turns")
        print(f"  Mutual defect    : {mutual_defect} turns")

    # ── Utility ───────────────────────────────────────────────────────

    @staticmethod
    def _header(title: str) -> str:
        width = 50
        return f"\n{'─' * width}\n  {title}\n{'─' * width}"
