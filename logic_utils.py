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
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


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

    # Happy path: both values are ints, so > is a numeric comparison.
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # Fallback: secret arrived as a str (e.g. from the even-attempt cast bug
        # in app.py that has since been fixed).  The original code converted guess
        # to str and compared strings, which gave wrong results for multi-digit
        # numbers — "9" > "10" is True lexicographically, flipping the hint.
        # Fix: convert both sides to int so the comparison is always numeric.
        if int(guess) == int(secret):
            return "Win", "🎉 Correct!"
        elif int(guess) > int(secret):
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
