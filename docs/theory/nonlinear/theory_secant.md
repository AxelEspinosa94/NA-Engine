
---

# Secant Method — Theory

The secant method approximates Newton’s method without requiring a derivative.

It solves:

\[
f(x) = 0
\]

using two initial guesses.

---

# 1. Iteration Formula

Given \( x_0 \) and \( x_1 \):

\[
x_{k+1} =
x_k - f(x_k)\frac{x_k - x_{k-1}}{f(x_k) - f(x_{k-1})}
\]

This replaces the tangent line with a secant line.

---

# 2. Convergence

- Faster than bisection  
- Slower than Newton  
- Convergence order ≈ 1.618 (golden ratio)

Fails when:

- Denominator is zero  
- Function is flat  
- Initial guesses are poor  

---

# 3. Stopping Criterion

\[
|x_{k+1} - x_k| < \text{tol}
\]

---

# 4. Properties

### Advantages
- No derivative required
- Faster than bisection
- Simple to implement

### Disadvantages
- Not guaranteed to converge
- Requires two initial guesses
- Can fail if denominator is small

---

# 5. Conceptual Example

Solve:

\[
x^2 - 2 = 0
\]

Start with:

\[
x_0 = 1,\quad x_1 = 2
\]

The method converges to:

\[
\sqrt{2} \approx 1.41421356
\]

---

# End of Document

