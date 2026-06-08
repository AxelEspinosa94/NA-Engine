
---

# Simpson’s Rules — Theory

Simpson’s rules approximate integrals using quadratic or cubic polynomials.  
They are significantly more accurate than the trapezoid rule.

---

# 1. Simpson 1/3 Rule

Requires **even** number of subintervals \( n \).

Let:

\[
h = \frac{b - a}{n}
\]

Then:

\[
S = \frac{h}{3}
\left[
f(x_0) + f(x_n)
+ 4\sum_{\text{odd}} f(x_i)
+ 2\sum_{\text{even}} f(x_i)
\right]
\]

This corresponds to fitting parabolas over pairs of intervals.

---

# 2. Simpson 3/8 Rule

Requires \( n \) to be a **multiple of 3**.

\[
S = \frac{3h}{8}
\left[
f(x_0) + f(x_n)
+ 3\sum_{i\not\equiv 0\ (3)} f(x_i)
+ 2\sum_{i\equiv 0\ (3)} f(x_i)
\right]
\]

This rule fits cubic polynomials over groups of three intervals.

---

# 3. Properties

### Advantages
- High accuracy (order \( O(h^4) \))
- Works well for smooth functions
- Composite versions are efficient

### Disadvantages
- Requires specific constraints on \( n \)
- Not ideal for functions with discontinuities

---

# 4. Conceptual Example

For:

\[
f(x) = x^2,\quad [0, 2],\quad n = 4
\]

Simpson 1/3 gives:

\[
S = 2.6666667
\]

which matches the exact integral:

\[
\frac{8}{3}
\]

---

# End of Document

