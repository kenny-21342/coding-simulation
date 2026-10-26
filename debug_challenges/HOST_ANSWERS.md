# Answers (for hosts only, don't leave this open on the screen)

| # | Bug | Fix | What it teaches |
|---|---|---|---|
| 1 | `vy -= GRAVITY * dt` | `vy += GRAVITY * dt` | Screen y points **down**, so gravity adds to y-speed. Sign errors are the most common physics bug. |
| 2 | Right wall: `vx = vx * BOUNCINESS` | `vx = -vx * BOUNCINESS` | Bouncing = reversing the velocity. Without the minus sign the ball keeps pushing into the wall and slides along it. |
| 3 | `math.cos(ANGLE)` and `math.sin(ANGLE)` with ANGLE in degrees | `math.cos(math.radians(ANGLE))` and `math.sin(math.radians(ANGLE))` | Python's trig functions use radians. 45 "radians" is about 2578°, so the shot goes in a strange direction, and at 50° it fires into the ground. |
| 4 | `velocty -= THRUST * dt` (typo) | `velocity -= THRUST * dt` | `NameError` tracebacks give the line number and even suggest the right name. Read the error before touching the code. |
| 5 | `if n == 2 or 3:` | `if n == 2 or n == 3:` (or `if n in (2, 3):`) | Python reads it as `(n == 2) or 3`, and `3` is always "truthy", so every live cell survives. No error is shown, so you find it by reasoning about behaviour. |

**Good questions to ask after a fix**
- 1: "What would happen on the Moon? Change GRAVITY and check."
- 2: "What does BOUNCINESS = 0.5 do now?"
- 3: "Which angle goes furthest? Is it the same as the formula predicts?"
- 5: "Change the survival rule to `n in (1, 2, 3)`. What happens?"
