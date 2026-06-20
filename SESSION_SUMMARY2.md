# Session Summary

## Date
2026-06-20

## What We Did

### Refactored `update_score` from `app.py` into `logic_utils.py`

The function was defined in `app.py` but belonged in `logic_utils.py`, which already had a stub raising `NotImplementedError`. We moved the implementation there and updated the import in `app.py`.

### Fixed the score bug in `update_score`

**Bug 1 — "Too High" inconsistently rewarded wrong guesses:**
On even-numbered attempts, guessing too high added +5 points instead of subtracting. The fix makes both `"Too High"` and `"Too Low"` always deduct 5 points.

```python
# Before (buggy)
if outcome == "Too High":
    if attempt_number % 2 == 0:
        return current_score + 5  # wrong: rewarding a bad guess
    return current_score - 5

# After (fixed)
if outcome in ("Too High", "Too Low"):
    return current_score - 5
```

**Bug 2 — Win formula off-by-one:**
The win points formula used `attempt_number + 1`, which meant a first-attempt win gave 80 points instead of 100. Changed to `attempt_number - 1`.

```python
# Before
points = 100 - 10 * (attempt_number + 1)

# After
points = 100 - 10 * (attempt_number - 1)
```

## Files Changed

| File | Change |
|------|--------|
| `logic_utils.py` | Replaced `update_score` stub with fixed implementation |
| `app.py` | Added `update_score` to import; removed local function definition |

## Remaining FIXMEs in `app.py`

These were noted but not addressed this session:

- **Line 56** — `attempts` initializes to `1` instead of `0`, which could cause an off-by-one in attempt counting on the first game load.
- **Line 121** — On even-numbered attempts, `secret` is cast to a string before being passed to `check_guess`, causing type-mismatch comparison bugs.
