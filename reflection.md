# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

---

## 1. What was broken when you started?

When I first ran the game, it loaded without crashing but immediately showed something suspicious: the attempts counter said "Attempts left: 7" even though I hadn't made a single guess yet — the sidebar clearly stated 8 attempts allowed. Opening the Developer Debug Info tab revealed the secret number (46), which let me test the hints deliberately rather than guessing blindly. The most obvious bug appeared right away: every hint was the opposite of what it should be — guessing lower than the secret told me to go lower, and guessing higher told me to go higher. The history panel also showed phantom entries (`""` and `"Default"`) that were never real guesses, which explained the missing attempt. Finally, the score displayed as a negative number the entire game (-5, -10, -15), then flipped to a positive on the win screen (Final score: 15), indicating the scoring logic had a sign error somewhere.

**Concrete bugs noticed at the start:**

- **Inverted hints** — the Higher/Lower feedback was backwards for every guess made.
- **Phantom history entries** — the game pre-populated the guess history with empty and "Default" values before any real input, consuming attempts incorrectly.

---

**Bug Reproduction Log**

| Input                                  | Expected Behavior                          | Actual Behavior                                                                                       | Console Output / Error |
| -------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------- |
| Guess of 21, Secret is 46              | "Go HIGHER" hint (21 < 46, need to go up)  | "Go LOWER!" displayed instead                                                                         | none                   |
| Guess of 80, Secret is 46              | "Go LOWER" hint (80 > 46, need to go down) | "Go HIGHER!" displayed instead                                                                        | none                   |
| Fresh game load, no guesses submitted  | Attempts left: 8, History empty            | Attempts left: 7, History contains `""` and two `"Default"` phantom entries                           | none                   |
| Guess of 46 (exact secret), win screen | Score shown consistently throughout game   | Debug panel showed Score: -15 during play; win screen displayed Final score: 15 (sign flipped on win) | none                   |

---

## 2. How did you use AI as a teammate?

I used the AI coding assistant built into VS Code as my main teammate for the repair work, giving it multi-step instructions while reviewing every diff before accepting it.

**A correct suggestion:** I gave the AI a multi-step prompt asking it to fix the `attempts` initialization (from 1 to 0), remove the block in `app.py` that converted the secret to a string on even attempts, refactor all four functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from `app.py` into `logic_utils.py`, fix the swapped hint messages inside `check_guess`, and update the import in `app.py`. The AI applied all of these correctly. I verified the result two ways: I read the diff for both files to confirm the `check_guess` messages were now correct ("Too High" → "Go LOWER!", "Too Low" → "Go HIGHER!") and that the function definitions were removed from `app.py` and replaced by a single import line, and then I ran the game live and confirmed the hints pointed in the right direction in both directions.

**An incorrect/misleading gap:** When the AI moved `update_score` into `logic_utils.py`, it copied the function over as expected but left the flawed scoring logic untouched — specifically the branch where a "Too High" outcome on an even-numbered attempt _adds_ 5 points instead of subtracting, which is why the score behaved inconsistently. The AI did not flag this as a bug or offer to fix it, even though it was clearly part of the broken scoring behavior I documented in Phase 1. I caught it by reviewing the diff against my own bug notes rather than trusting that "refactor this function" also meant "fix everything wrong with it." This was a useful reminder that the AI does exactly what you ask and no more — it won't volunteer judgment about correctness unless you direct it to.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only after it passed two independent checks: a manual play-through and an automated test. For the manual check I opened the Developer Debug Info tab to see the secret number, then deliberately guessed above and below it to confirm the hint direction was correct in both cases, and confirmed a fresh game now started at "Attempts left: 8" with an empty history. For automated verification, I asked the AI to generate `pytest` cases in `tests/test_game_logic.py` targeting the exact bugs I fixed — for example `test_check_guess_too_high`, which guesses 80 against a secret of 50 and asserts the outcome is "Too High" and that the word "LOWER" appears in the message. I ran `pytest` and all 5 tests passed, which proved the comparison logic and the parsing logic both behaved correctly. AI helped design the tests by turning my plain-language descriptions of each bug into concrete assertions, but I reviewed each test first to make sure the expected values actually matched correct game behavior rather than just blindly trusting the generated code.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
