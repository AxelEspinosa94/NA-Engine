
---

# Newton’s Method — Theory

Newton’s method is a root‑finding algorithm that uses tangent lines to approximate solutions of:

$$
f(x) = 0
$$

---

# 1. Iteration Formula

Starting from $x_0$:

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$

This is derived from the tangent line approximation.

---

# 2. Convergence

If $f$ is smooth and the initial guess is close to the root:

- Convergence is **quadratic**
- Very fast compared to other methods

Fails when:

- $f'(x_k) = 0$
- Derivative is small or undefined
- Initial guess is poor

---

# 3. Stopping Criterion

$$
|x_{k+1} - x_k| < \text{tol}
$$

---

# 4. Properties

### Advantages
- Extremely fast (quadratic convergence)
- Very accurate

### Disadvantages
- Requires derivative
- Can diverge if starting point is poor
- Fails when derivative is zero

---

# 5. Conceptual Example

Solve:

$$
f(x) = x^2 - 2
$$

Iteration:

$$
x_{k+1} = \frac{x_k + 2/x_k}{2}
$$

Converges rapidly to:

$$
\sqrt{2} \approx 1.41421356
$$

---

# End of Document

