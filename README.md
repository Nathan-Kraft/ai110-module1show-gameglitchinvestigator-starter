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


- [ ] Explain what fixes you applied.


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```

pytest tests/
 ========================= 36 passed in 0.06s =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
