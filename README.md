# Simulations: code and play

**Physics and CS in the Spotlight · 11/16 to 11/19, lunch, outside the canteen**
Run by Mr. Victorio, Kenny and CS students.

Visitors play with physics simulations on the big screen, change the code to see what happens,
fix buggy programs, and learn to prompt AI to build a simulation of their own.

```
coding-simulation/
├── launcher.py              ← start here: menu of all simulations (big screen)
├── sims/                    ← 6 simulations, each with a PLAY WITH ME section at the top
│   ├── 01_projectile.py
│   ├── 02_bouncing_balls.py
│   ├── 03_orbits.py
│   ├── 04_pendulum_painting.py
│   ├── 05_resonance_string.py
│   └── 06_game_of_life.py
├── debug_challenges/        ← 5 programs with one bug each + hint cards
│   ├── README.md            (hints, safe to show students)
│   └── HOST_ANSWERS.md      (answers, hosts only)
└── ai_station/
    ├── PROMPT_CARDS.md      ← print this for the AI station
    └── starter_template.py
```

---

## 1. Setup (do this before 11/16, on every laptop)

1. Install **Thonny** from **thonny.org**. It's a free Python editor with Python built in and a simple step-by-step debugger, so it's good for beginners.
2. Open Thonny → **Tools → Manage packages…** → search **pygame** → **Install**.
3. Copy the whole `coding-simulation` folder onto the laptop.
4. In Thonny, open `launcher.py` and press **Run** (green ▶). The menu should appear.
5. Open each simulation once to check it runs, then try one bug challenge.

Already have Python? `pip3 install pygame` in Terminal works too, then `python3 launcher.py`.

---

## 2. Station layout (3 zones)

| Zone | Equipment | What visitors do | Hosts |
|---|---|---|---|
| **A. Play** | Big screen + laptop running `launcher.py` (press **F** for fullscreen) | Try the simulations with keyboard and mouse | 1 |
| **B. Tweak and debug** | 1–2 laptops with Thonny open | Change PLAY WITH ME numbers; fix the bug challenges | 1–2 |
| **C. Ask AI** | 1 laptop with the school's AI tool + Thonny, and printed `PROMPT_CARDS.md` | Prompt AI to build a simulation, run it, check it | 1 |

Lunch is short, so aim for **about 5 minutes per visitor per zone**. A visitor who finishes a bug challenge or gets an AI simulation running can collect a stamp in the companion app (station code **CODE**).

---

## 3. What hosts can say

**Zone A (hook):** "Pick a planet and fire the cannon. Can you hit the white arrow? That's where the formula says it lands."

**Zone B (tweak):** "Everything you just played with is controlled by these numbers at the top. Change one, press Run, and see what happens."
Good first changes:
- `01_projectile.py`: `GRAVITY = 1.62` (the Moon) or `AIR_RESISTANCE = 0.1`
- `02_bouncing_balls.py`: `BOUNCINESS = 1.0` (energy stays at 100%), then `1.1` (where does the extra energy come from?)
- `03_orbits.py`: `PLANETS_PULL_EACH_OTHER = True`
- `05_resonance_string.py`: `DAMPING = 0.02`, then find a harmonic
- `06_game_of_life.py`: `BORN_WITH = {3, 6}` (HighLife) or `BORN_WITH = {2}` and `SURVIVE_WITH = set()` (Seeds)

**Zone B (debug):** "This program has one mistake. What's it doing wrong? Let's find the line." Hints are in `debug_challenges/README.md`. Point to the hint before giving the answer.

**Zone C (AI):** "AI writes the code, but you're the scientist: you check it's right." Use the master prompt, then go through the checklist at the bottom of the prompt cards together.

---

## 4. What each simulation shows

| Simulation | Physics or CS idea | Something to try |
|---|---|---|
| Projectile | Equations of motion, R = v² sin 2θ / g, air resistance | Which angle goes furthest? Does that change with air on? |
| Bouncing balls | Momentum, collisions, energy loss | Watch the energy bar fall with bounciness below 1 |
| Orbits | Newton's gravity, circular and escape speed | Drag slowly, then fast. The label shows the speed needed for a circle and to escape |
| Pendulum painting | Damped oscillations, frequency ratios, Lissajous figures | Presets 1–5; ratios close to simple fractions make neat shapes |
| Resonance | Standing waves, harmonics, damping | Press 1–6 for harmonics, then 0.05 Hz off. Count the nodes |
| Game of Life | Cellular automata, emergence | Press G for a glider gun; change the rules |

Every simulation: **F** fullscreen, **ESC** quit (back to the launcher).

---

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | Install pygame in Thonny: Tools → Manage packages |
| Window opens but the keyboard does nothing | Click once inside the simulation window to give it focus |
| Fullscreen looks stretched or stuck | Press F again, or ESC to quit and reopen |
| A visitor broke a file while editing | Undo with ⌘Z, or copy a clean file from your backup USB |
| Pendulum painting PNGs pile up | They save into `sims/`; delete them after the event |

Keep a **clean backup copy** of the folder on a USB drive. Visitors will edit the files!
