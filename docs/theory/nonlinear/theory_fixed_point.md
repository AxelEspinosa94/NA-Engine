
---

# Fixed Point Iteration — Theory

Fixed point iteration solves equations of the form:

$$
f(x) = 0
$$

by rewriting them as:

$$
x = g(x)
$$

A solution $x^\*$ is a **fixed point** of $g$:

$$
g(x^\*) = x^\*
$$

---

# 1. Iteration Formula

Given an initial guess $x_0$:

$$
x_{k+1} = g(x_k)
$$

---

# 2. Convergence Condition

A fixed point is **locally convergent** if:

$$
|g'(x^\*)| < 1
$$

If:

$$
|g'(x^\*)| > 1
$$

the method diverges.

---

# 3. Stopping Criterion

$$
|x_{k+1} - x_k| < \text{tol}
$$

---

# 4. Properties

### Advantages
- Very simple
- No derivatives required
- Works when a suitable $g(x)$ is available

### Disadvantages
- Requires a convergent transformation
- Slow convergence (linear)
- Sensitive to the choice of $g(x)$

---

# 5. Conceptual Example

Solve:

$$
x^2 - 2 = 0
$$

Rewrite as:

$$
x = \sqrt{2}
\quad\Rightarrow\quad
g(x) = \sqrt{2}
$$

Iteration converges to:

$$
x^\* \approx 1.41421356
$$

---

# End of Document

