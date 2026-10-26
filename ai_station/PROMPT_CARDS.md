# Ask AI to build a simulation

Use the AI tool your school allows. Copy the **master prompt**, fill in the blanks, paste it in,
then copy the code it gives you into a new file in Thonny and press **Run**.

---

## The master prompt

> Write a Python program using **pygame** that simulates **[WHAT YOU WANT TO SEE]**.
>
> Rules:
> - Put every number I might want to change at the top, under a comment that says `# PLAY WITH ME`, with a short comment explaining each one and its units.
> - Window size 1280 x 720, dark background, show the controls as text at the bottom of the window.
> - Show the important values on screen (for example speed, height, energy).
> - ESC quits. Keep it under 150 lines and use only pygame, math and random.
> - Add short comments explaining the physics in each step.
>
> After the code, explain in 3 sentences which physics equation the program uses.

**Why this works:** it says *what* to build, *how* it should look, *what limits* to stick to, and *what to explain*.
A vague prompt ("make a physics game") gets a vague program.

---

## Idea cards (fill in the blank)

| Card | Fill in "WHAT YOU WANT TO SEE" with… | Physics or CS |
|---|---|---|
| 🚀 Lunar lander | a lander falling onto the Moon; the UP key fires a thruster that uses fuel; land gently to win | forces, gravity |
| 🌀 Spring | a mass bouncing on a spring, with a graph of its height over time drawn live | simple harmonic motion |
| 🎯 Pinball | a pinball machine with two flippers controlled by the LEFT and RIGHT keys | collisions, angles |
| 🌊 Ripples | two sources of circular waves on a pond and the interference pattern they make | waves, interference |
| 🔥 Gas in a box | 100 tiny particles bouncing in a box; a slider for temperature changes their speed; show the pressure on the walls | kinetic theory |
| 🧲 Charges | positive and negative charges I can place by clicking, with field lines drawn between them | electric fields |
| 🚗 Traffic | cars on a circular road that brake when the car in front is close; show how traffic jams appear by themselves | modelling, emergence |
| 🐇 Foxes and rabbits | rabbits that breed and foxes that eat them, with a live graph of both populations | modelling, feedback |
| 🔀 Sorting race | bubble sort and quicksort sorting bars side by side, with a step counter for each | algorithms |

---

## When it doesn't work

**It crashed.** Copy the whole red error message and send:
> My program crashed with this error: **[PASTE ERROR]**. Explain what it means in simple words, then show only the lines I need to change.

**It runs but the physics looks wrong.** Describe what you see:
> The ball **[WHAT IT DOES]** but it should **[WHAT SHOULD HAPPEN]**. Find the bug and explain why it happened.

**You want to understand it.**
> Explain lines **[X to Y]** like I'm in Year 9. What would happen if I changed **[NUMBER]** to **[NEW NUMBER]**?

**You want to improve it.**
> Add **[a trail behind the ball / a pause key / a graph of energy / sound when it bounces]**. Show me the whole updated program.

---

## Check the AI's work (it can be wrong!)

AI writes code that *looks* right but sometimes isn't. Before you trust it:

- [ ] **Does it run?** No errors when you press Run.
- [ ] **Does it fall the right way?** On a screen, y gets bigger going *down*.
- [ ] **Do the units make sense?** Is gravity in pixels per second² or metres per second²? Does the program say?
- [ ] **Test one number you can check.** Set something to 0 (gravity, friction, speed). Does the program do what physics says it should?
- [ ] **Push it to extremes.** Very big or very small numbers. Does it break, or behave sensibly?
- [ ] **Can you explain one equation in it?** If not, ask the AI to explain it, then check that against your textbook.
