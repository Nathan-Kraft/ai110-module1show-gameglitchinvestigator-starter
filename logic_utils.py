def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.
    logic_utils.py:1-8 — get_range_for_difficulty is now implemented here.
    Hard difficulty now uses 1–500 (vs. the bugged 1–50 which was actually easier than Normal's 1–100).
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


"""
logic_utils.py — check_guess stub replaced with the full implementation.
Bug fixed: when guess > secret the hint now correctly says "Go LOWER!" (was "Go HIGHER!"), and when guess < secret it says "Go HIGHER!" (was "Go LOWER!").
app.py — added from logic_utils import check_guess at the top and removed the old function definition.
"""
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        elif g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"

"""
logic_utils.py — replaced the NotImplementedError stub with the fixed update_score implementation
(consistent -5 for both wrong outcomes, fixed win formula off-by-one).
"""
def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
