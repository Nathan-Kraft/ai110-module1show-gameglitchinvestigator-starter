def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500  # Fix: was 1–50, making Hard easier than Normal (1–100); corrected to 1–500
    return 1, 100


# Fix: function was a NotImplementedError stub; moved the real implementation here from app.py
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # Fix: original had two separate if-blocks for None and ""; merged into one condition
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


# Fix: messages were swapped — guess > secret said "Go HIGHER!" and guess < secret said "Go LOWER!".
# Corrected by swapping the return strings so each hint points the player in the right direction.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"  # Fix: was "Go HIGHER!" — now correctly tells player to go lower
        else:
            return "Too Low", "📈 Go HIGHER!"  # Fix: was "Go LOWER!" — now correctly tells player to go higher
    except TypeError:
        # Fix: original code cast guess to str and used string comparison, which breaks for
        # multi-digit numbers ("9" > "10" is True lexicographically). Now both sides are
        # cast to int so the comparison is always numeric.
        if int(guess) == int(secret):
            return "Win", "🎉 Correct!"
        elif int(guess) > int(secret):
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"

# Fix: removed the `attempt_number % 2 == 0` branch that awarded +5 for "Too High" on even attempts.
# Fix: win formula used `attempt_number + 1` (off-by-one); corrected to `attempt_number - 1`.
# Both wrong-guess outcomes now consistently subtract 5.
def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)  # Fix: was (attempt_number + 1), over-penalising early wins
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):  # Fix: was two separate branches; "Too High" on even attempts added +5 instead of -5
        return current_score - 5

    return current_score
