from logic_utils import check_guess, update_score, get_range_for_difficulty

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
