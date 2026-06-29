# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

  **Game Glitch Investigator: The Impossible Guesser** is an educational debugging exercise disguised as a broken number-guessing game. The player's goal is to guess a randomly chosen secret number, but the game has been intentionally shipped with bugs — the secret number resets on every guess, and the "Higher/Lower" hints are inverted — making it impossible to win in its broken state.

  The real purpose of the game is to teach players how to diagnose and fix common bugs in a Python/Streamlit application: specifically, understanding Streamlit's session state model (why variables reset on re-render) and identifying inverted conditional logic. After finding and fixing all the bugs, players refactor the core logic into a separate module and validate their fixes with a pytest test suite.

- [ ] Detail which bugs you found.

Hints

check_guess in app.py (originally inline) had the hint messages swapped — guessing too high said "Go HIGHER!" and too low said "Go LOWER!"
check_guess in app.py (originally inline) was comparing values as strings instead of integers, which caused lexicographic comparisons and broke hints for multi-digit numbers

Scoring

update_score in app.py (originally inline) had a branch that added +5 to the score on even attempts when the guess was "Too High" instead of subtracting 5
update_score in app.py (originally inline) win formula used attempt_number + 1 instead of attempt_number - 1, over-penalizing early wins
app.py lines 74–79 — the new game block was missing st.session_state.score = 0, causing score to accumulate across sessions

Attempts

app.py — st.session_state.attempts was initialized to 1 instead of 0, making the first guess miscounted and the remaining attempts display off by one

Difficulty / Range

app.py (originally inline) — get_range_for_difficulty was returning incorrect ranges; Easy was not constrained to 1–20 and Hard was set to 1–50 instead of a range larger than Normal
app.py — the secret was generated using the default range instead of the difficulty-specific one, so secrets fell outside the expected bounds

Game Restart

app.py lines 74–79 — the new game block only set a new secret but did not reset score, attempts, status, or history, so the UI appeared stuck after restarting

- [ ] Explain what fixes you applied.
For more detailed explanations of check_guess see session_summary.md file.
For more detailed explanations of fixes for update score see session_summary2.md

Hints

Swapped the return strings in check_guess so "Too High" says "Go LOWER!" and "Too Low" says "Go HIGHER!"
Cast both guess and secret to int inside check_guess so comparisons are always numeric, never lexicographic

Scoring

  Removed the attempt_number % 2 == 0 branch in update_score that was adding +5 on even attempts; both "Too High" and "Too Low" now consistently subtract 5
  Fixed the win formula in update_score from 100 - 10 * (attempt_number + 1) to 100 - 10 * (attempt_number - 1)
  Added st.session_state.score = 0 to the new game block in app.py so the score resets on each new game.

Attempts

  Changed the initial value of st.ession_stateattempts from 1 to 0 in app.py

Difficulty / Range

  Moved get_range_for_difficulty into logic_utils.py and corrected the ranges — Easy: 1–20, Normal: 1–100, Hard: 1–500.
  Moved update_score into logic_utils.py and updated the import in app.py

Game Restart

  Added st.session_state.score, st.session_state.attempts, st.session_state.status, and st.session_state.history resets to the new game block, followed by st.rerun() to force a clean rerun.


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Starts hard difficulty setting game. user enters 250. 
2. Game returns "Go Lower" so guess is too high 
3. user enters 200 for guess 
4. Game returns "Go Lower" so guess is too high
5. User enters 150 for guess
5. Game returns "Go Lower" so guess is too high
6. User enters 128 for guess
7. Game returns "correct" so secret was 128, user recieved a final score of 55. 

![Screenshot of Fixed game and results from the Demo Walkthrough](ai110-module1show-gameglitchinvestigator-starter\finished_screenshot.png)


## 🧪 Test Results

```
pytest tests/
 ========================= 36 passed in 0.06s =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
