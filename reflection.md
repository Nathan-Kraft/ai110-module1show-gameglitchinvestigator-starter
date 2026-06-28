# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

- List at least two concrete bugs you noticed at the start  
You are not able to restart the game. At least the UI doesn't show the game restarting the developer pannel does show a new secret but the rest seem to not reset. 
The Hints seem to be opposite of what they should be. 
number of available attempts is off by 1. 

  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
50       go Lower             Go higher         secret 31/hint telling me to go higher when it should have said to go lower. No console errors

10                                              Secret is out of range despite being on easy mode secret is set to 50 when range is supposed to be 1-20. No console errors
30                                              Secret is out of range despite being on Hard mode secret is set to 56 when range is supposed to be 1-50. Also the hard mode should have a bigger range than normal mode. No console errors


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude Code with the vscode extension. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
When I asked claude to "Move the update_score function to logic_utils.py, update the logic to fix the score bug, and update the import in app.py." after then asking it to show me in detail of what it was going to change, it showed the change in code. Where it fixed the bug of a "too high" guess would inconsistently adding 5 to the score on even attempts. It removed the chunck causing the error and made it so that every wrong guess would be -5 to the score. I then had it add pytests for this which I read through and then it passed all. When I run the game it correctly updates the current score and displays the final score correctly. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The AI gave me pytests that were set up correctly for the check_guess function, providing that the check_guess function was implemented correctly in the first place. However the AI originally left the function to compare strings, which would only compare the first digit of the string, which would then cause the error of the hints. I didn't catch this at first so when I tried to run my pytests I found that it would always fail. I then asked the AI why it was failing and then it investigated and found the error within the check_guess funtion and fixed it in the logic_utils.py file. I would call this an incorrect suggestion cause it suggested changes that later were found to cause issues. After running the game I haven't seen an issue arise from this since. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  After fixing the code I used the AI to create the pytests which then the code passed all tests. After that I have ran the game multiple times trying to recreate the issue and I never couldn't get it to reapper, so I then considered the bug fixed. 

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
test_int_and_string_secret_produce_same_outcome verifies that check_guess produces the same result regardless of whether the secret number is passed as an integer or a string. The bug it guards against is a type-casting issue where, if the secret is stored as a string, Python compares values lexicographically instead of numerically. Lexicographic order differs from numeric order whenever one number has more digits than the other.
The test runs three pairs that specifically hit this edge case (9 vs 10, 99 vs 100, 19 vs 20), calls check_guess twice for each, once with an int secret and once with the same value as a str, and asserts both calls return the same outcome. If they differ, it means the function is doing a string comparison somewhere instead of a numeric one.
What I found out about my code after making this test with the AI is that the check_guess funtion was doing a string comparison still, and neither me nor Claude noticed it until after we created the tests and ran them. I then fixed the issue and now everything runs correctly. 

- Did AI help you design or understand any tests? How?
  Claude helped me design the pytests and helped me with understanding multiple that I didn't understand. Whenever I asked Claude to give me more information or explain the tests it wanted to implement it would go into detail for each one. When I made the tests for update score and found that all the tests for the string-cast secret on even attempts bug, they would all fail at first, I then had the AI help me understand why it failed which we found was an issue with the function, which I mentioned earlier. 
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


pet, plan, owner, constraint, 
