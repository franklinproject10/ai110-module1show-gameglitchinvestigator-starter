\# 🎮 Game Glitch Investigator: The Impossible Guesser

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
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game's purpose:** A single-player number guessing game built with Streamlit. The app picks a secret number within a range determined by difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player tries to guess it within a limited number of attempts. After each guess the game gives a higher/lower hint, tracks a running score, and ends when the player either guesses correctly or runs out of attempts.

**Bugs found:**

- **Inverted hints** — `check_guess` returned the wrong direction message: a guess that was too high told the player to "Go HIGHER!" and a guess that was too low told them to "Go LOWER!", making the game impossible to win by following the hints.
- **Secret type-switching** — on even-numbered attempts, `app.py` converted the secret number to a string before comparison, breaking the numeric comparison inside `check_guess` and triggering a fragile string-comparison fallback.
- **Attempts off-by-one** — `attempts` was initialized to `1` instead of `0`, so a fresh game displayed "Attempts left: 7" before the player had made a single guess.
- **Inconsistent scoring** _(noted, not fixed)_ — `update_score` adds points for some wrong guesses on even-numbered attempts, causing the score to behave unpredictably and the displayed value to appear to flip sign on a win.

**Fixes applied:**

- Corrected the swapped messages in `check_guess` so "Too High" returns "Go LOWER!" and "Too Low" returns "Go HIGHER!".
- Removed the block in `app.py` that converted the secret to a string on even attempts; the secret is now always passed to `check_guess` as an integer.
- Changed the `attempts` initialization from `1` to `0` so a fresh game correctly shows the full attempt count.
- Refactored all four core functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` and into `logic_utils.py`, with `app.py` now importing them — separating game logic from UI.
- Added automated `pytest` cases in `tests/test_game_logic.py` to lock in the corrected behavior.

## 📸 Demo Walkthrough

A sample game on Normal difficulty (range 1–100, 8 attempts), with the secret number 34 visible via the Developer Debug Info tab:

1. Game loads showing "Attempts left: 8" and an empty history — confirming the attempts counter starts correctly.
2. Player enters a guess of **46** → game returns "📉 Go LOWER!" (correct, since 46 > 34).
3. Player enters a guess of **21** → game returns "📈 Go HIGHER!" (correct, since 21 < 34).
4. The attempts counter and guess history update correctly after each guess (Attempts left drops 8 → 7 → 6, history records 46 then 21).
5. Player enters a guess of **34** → game returns "🎉 Correct!" and displays "You won! The secret was 34." ending the game.

**Screenshot** _(optional)_: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -q
.....                                                          [100%]
5 passed
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
