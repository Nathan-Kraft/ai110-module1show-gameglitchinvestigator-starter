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
50       go Lower             Go higher         secret 31/telling to go higher when it should have said to go lower.   

10                                              Secret is out of range despite being on easy mode secret is set to 50 when range is supposed to be 1-20.
30                                              Secret is out of range despite being on Hard mode secret is set to 56 when range is supposed to be 1-50. Also the hard mode should have a bigger range than normal mode. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The AI gave me pytests that were set up correctly for the check_guess function, providing that the check_guess function was implemented correctly in the first place. However the AI originally left the function to compare strings, which would only compare the first digit of the string, which would then cause the error of the hints. I didn't catch this at first so when I tried to run my pytests I found that it would always fail. I then asked the AI why it was failing and then it investigated and found the error within the check_guess funtion and fixed it in the logic_utils.py file. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

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
