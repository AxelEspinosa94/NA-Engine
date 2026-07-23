
---

# Bisection Method — Theory

The bisection method is a bracketing technique for solving:

$$
f(x) = 0
$$

It requires an interval $[a, b]$ such that:

$$
f(a)f(b) < 0
$$

meaning the function changes sign.

---

# 1. Iteration Formula

At each step:

$$
c = \frac{a + b}{2}
$$

Evaluate $f(c)$:

- If $f(a)f(c) < 0$, the root is in $[a, c]$
- Else, it is in $[c, b]$

---

# 2. Stopping Criteria

- $|f(c)| < \text{tol}$
- $|b - a| < \text{tol}$

---

# 3. Properties

### Advantages
- Guaranteed convergence
- Very robust
- Simple to implement

### Disadvantages
- Slow convergence (linear)
- Requires a sign change
- Not efficient for high precision

---

# 4. Conceptual Example

Solve:

$$
x^2 - 2 = 0
$$

Choose:

$$
a = 1,\quad b = 2
$$

Since:

$$
f(1) = -1,\quad f(2) = 2
$$

the method converges to:

$$
\sqrt{2} \approx 1.41421356
$$

---

# End of Document

