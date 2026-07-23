
---

# False Position (Regula Falsi) — Theory

The false position method is a hybrid of:

- Bisection (bracketing)
- Secant (linear interpolation)

It solves:

$$
f(x) = 0
$$

using an interval $[a, b]$ with:

$$
f(a)f(b) < 0
$$

---

# 1. Iteration Formula

$$
c = b - f(b)\frac{b - a}{f(b) - f(a)}
$$

This is the secant formula, but the interval is updated **while preserving the sign change**.

---

# 2. Stopping Criterion

$$
|f(c)| < \text{tol}
$$

---

# 3. Properties

### Advantages
- Guaranteed convergence (like bisection)
- Faster than bisection
- Uses linear interpolation

### Disadvantages
- Convergence may stall if one endpoint barely moves
- Slower than Newton and Secant

---

# 4. Conceptual Example

Solve:

$$
x^2 - 2 = 0
$$

Start with:

$$
a = 1,\quad b = 2
$$

The method converges to:

$$
\sqrt{2} \approx 1.41421356
$$

---

# End of Document

---
