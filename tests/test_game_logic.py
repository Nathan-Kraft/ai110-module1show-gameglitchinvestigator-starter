import pytest
from logic_utils import check_guess, update_score, get_range_for_difficulty, parse_guess

def test_winning_guess():
    # Fixed: check_guess returns a tuple (outcome, message); unpack instead of comparing the whole tuple to a string
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Fixed: same tuple-unpacking fix as test_winning_guess
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # Fixed: same tuple-unpacking fix as test_winning_guess
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- check_guess hint message direction tests ---
# These tests target the original bug where the hint messages were swapped:
# guessing too high told the player to go higher, and vice versa.

def test_too_high_message_says_go_lower():
    # When guess (80) exceeds the secret (50), the player needs to go lower.
    # The original bug returned "Go HIGHER!" here, sending the player further away.
    _, message = check_guess(80, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_message_says_go_higher():
    # When guess (20) is below the secret (50), the player needs to go higher.
    # The original bug returned "Go LOWER!" here, sending the player further away.
    _, message = check_guess(20, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


# --- check_guess string-secret branch (TypeError path) ---
# app.py bug: on even-numbered attempts the secret was cast to str before being
# passed to check_guess (e.g. check_guess(50, "50") instead of check_guess(50, 50)).
# This exercises the except TypeError branch and confirms it behaves correctly.

def test_win_with_string_secret():
    # A correct guess must still produce a "Win" outcome even when the secret
    # arrives as a string due to the even-attempt cast bug in app.py.
    outcome, _ = check_guess(50, "50")
    assert outcome == "Win"

def test_too_high_with_string_secret_message():
    # The hint direction must be correct through the TypeError branch too —
    # guessing 80 against a string secret "50" should still say Go LOWER.
    _, message = check_guess(80, "50")
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_with_string_secret_message():
    # Likewise, guessing 20 against a string secret "50" should say Go HIGHER,
    # not Go LOWER as the original swapped-message bug would have produced.
    _, message = check_guess(20, "50")
    assert "HIGHER" in message
    assert "LOWER" not in message


# --- update_score tests ---

def test_win_first_attempt():
    # First attempt win should give full 100 points
    assert update_score(0, "Win", 1) == 100

def test_win_second_attempt():
    # Each additional attempt costs 10 points
    assert update_score(0, "Win", 2) == 90

def test_win_score_never_below_10():
    # Win bonus is capped at a minimum of 10
    assert update_score(0, "Win", 100) == 10

def test_too_high_always_subtracts():
    # Bug was: even attempts used to ADD 5 instead of subtracting
    assert update_score(50, "Too High", 2) == 45  # was 55 before the fix
    assert update_score(50, "Too High", 3) == 45

def test_too_high_even_attempt_subtracts():
    # Original bug: the update_score function had an attempt_number % 2 == 0 branch
    # that added +5 for "Too High" on even attempts instead of subtracting.
    # Attempt 2 is even — the buggy code returned 55, the fixed code returns 45.
    assert update_score(50, "Too High", 2) == 45

def test_too_low_subtracts():
    assert update_score(50, "Too Low", 1) == 45

def test_wrong_guess_outcomes_are_equal():
    # "Too High" and "Too Low" should have the same score impact
    assert update_score(50, "Too High", 2) == update_score(50, "Too Low", 2)

def test_too_high_and_too_low_have_equal_penalty():
    # Before the fix, "Too High" on even attempts added +5 while "Too Low" always
    # subtracted 5 — the two outcomes had asymmetric penalties. This test confirms
    # both now deduct the same amount regardless of attempt number.
    assert update_score(50, "Too High", 2) == update_score(50, "Too Low", 2)

def test_unknown_outcome_leaves_score_unchanged():
    # The catch-all return at the end of update_score should leave the score
    # untouched for any outcome string that isn't "Win", "Too High", or "Too Low".
    # Guards against future typos or new outcome values silently changing the score.
    assert update_score(50, "Bogus", 1) == 50


# --- get_range_for_difficulty tests (bug: new_game used hardcoded 1-100 instead of difficulty range) ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 500)

def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)

def test_easy_range_is_narrower_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high

def test_hard_range_is_wider_than_normal():
    # Original bug: Hard returned (1, 50), which is narrower than Normal's (1, 100),
    # making Hard the easiest difficulty instead of the hardest. This asserts that
    # Hard's upper bound is strictly greater than Normal's.
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

def test_hard_was_not_bugged_50():
    # Pins the exact wrong value from the original bug (50) so that any regression
    # back to (1, 50) fails immediately with a specific number rather than a vague
    # comparison failure.
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high != 50

def test_hard_range_is_wider_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

def test_easy_high_not_same_as_hardcoded_bug():
    # Bug used randint(1, 100) for all difficulties; Easy should cap at 20, not 100
    _, easy_high = get_range_for_difficulty("Easy")
    assert easy_high != 100

def test_hard_high_not_same_as_hardcoded_bug():
    # Bug used randint(1, 100) for all difficulties; Hard should go to 500, not 100
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high != 100

"""
Tests that specifically target the three bugs fixed in this session:

  Bug 1 — parse_guess raised NotImplementedError (stub was never filled in).
  Bug 2 — st.session_state.attempts was initialised to 1 instead of 0,
           causing the first turn to report one fewer remaining attempt than
           the player actually had.  (Streamlit session state cannot be unit-
           tested without a full app harness, so this bug is documented here
           but not exercised via pytest.)
  Bug 3 — On every even-numbered attempt, app.py cast the int secret to str
           before passing it to check_guess.  For multi-digit secrets this
           produces wrong comparisons: "9" > "10" is True lexicographically,
           so check_guess(9, "10") would return "Too High" instead of "Too Low".
"""


# ---------------------------------------------------------------------------
# Bug 1 — parse_guess was a NotImplementedError stub
# ---------------------------------------------------------------------------

def test_parse_guess_does_not_raise():
    # Before the fix, calling parse_guess raised NotImplementedError immediately.
    # Any call at all would crash; a valid input is sufficient to confirm the
    # stub has been replaced with a real implementation.
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_decimal_string_truncates_to_int():
    # "3.7" should parse to 3, not raise an error.
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_guess_none_and_empty_produce_same_outcome():
    # The original app.py had two separate if-blocks for None and ""; the merged
    # version must behave identically for both.
    none_result = parse_guess(None)
    empty_result = parse_guess("")
    assert none_result == empty_result


# ---------------------------------------------------------------------------
# Bug 3 — secret cast to str on even attempts breaks check_guess comparisons
# ---------------------------------------------------------------------------

def test_int_secret_too_low_two_digit():
    # Canonical case: guess=9, secret=10 as integers.
    # 9 < 10, so the outcome must be "Too Low".
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"


def test_string_secret_lexicographic_trap():
    # This is the exact failure the even-attempt bug introduced.
    # Lexicographically "9" > "10" (because "9" > "1"), so a naive string
    # comparison returns "Too High".  check_guess must return "Too Low" here
    # regardless of whether the secret arrives as int or str.
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low", (
        'check_guess(9, "10") returned "Too High" — '
        "string comparison \"9\" > \"10\" is True, which is the even-attempt cast bug"
    )


def test_string_secret_hint_direction_correct():
    # The hint message must also point the right way through the TypeError branch.
    _, message = check_guess(9, "10")
    assert "HIGHER" in message
    assert "LOWER" not in message


def test_int_and_string_secret_produce_same_outcome():
    # After the fix, passing the secret as int vs str should produce the same
    # outcome for a range of values where lexicographic order differs from
    # numeric order (all pairs where guess has more digits than secret, or vice
    # versa, are the interesting edge cases).
    pairs = [
        (9, 10),    # "9" > "10" lexicographically — classic trap
        (99, 100),  # "99" > "100" lexicographically
        (19, 20),   # "19" > "20" is False, but exercises the branch
    ]
    for guess, secret in pairs:
        int_outcome, _ = check_guess(guess, secret)
        str_outcome, _ = check_guess(guess, str(secret))
        assert int_outcome == str_outcome, (
            f"check_guess({guess}, {secret}) → {int_outcome!r} but "
            f"check_guess({guess}, '{secret}') → {str_outcome!r}"
        )
