# Debugging challenges

Each program has **one bug**. Run it, describe what goes wrong in your own words, then find the line and fix it.
Start with challenge 1. Only read a hint if you're stuck, and read them in order.

| Challenge | File | Difficulty |
|---|---|---|
| 1 | `bug_1_falling_up.py` | ★ |
| 2 | `bug_2_sticky_wall.py` | ★ |
| 3 | `bug_3_wonky_cannon.py` | ★★ |
| 4 | `bug_4_crash.py` | ★★ (it crashes: read the error!) |
| 5 | `bug_5_life_explodes.py` | ★★★ |

**How to debug like a programmer**
1. Say what *should* happen and what *actually* happens.
2. Look at the numbers printed on screen. Which one looks wrong?
3. Find the lines that change that number.
4. In Thonny, click **Debug** (the bug icon) and step through those lines one at a time to watch the values change.

---

## Hint cards

**Challenge 1: the ball falls up**
- Hint 1: Look at the comment in the code: on a screen, which way does y go when something moves down?
- Hint 2: Gravity should make `vy` bigger (downwards) every frame. Find the line that changes `vy` because of gravity.

**Challenge 2: the sticky wall**
- Hint 1: The left wall works. Compare the left-wall code with the right-wall code, line by line.
- Hint 2: After hitting the right wall the ball must start moving left. Which sign must `vx` have to move left?

**Challenge 3: the wonky cannon**
- Hint 1: The barrel is drawn correctly. Compare how the barrel's angle is calculated with how the ball's speed is calculated.
- Hint 2: Python's `math.sin` and `math.cos` don't use degrees. What do they use?

**Challenge 4: the crash**
- Hint 1: The last line of the red error message says what went wrong. The line above it shows where.
- Hint 2: Read the variable name in the error letter by letter, then compare it with the name used everywhere else.

**Challenge 5: life that never dies**
- Hint 1: Live cells never die, so look at the code that decides whether a live cell survives.
- Hint 2: Try this in the Shell: type `n = 7` and then `n == 2 or 3`. Is the answer what you expected? Why?
