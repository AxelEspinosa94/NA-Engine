
---

# Romberg Integration — Theory

Romberg integration is an extrapolation technique that builds upon the trapezoid rule to achieve very high accuracy.

It constructs a triangular table of increasingly accurate estimates.

---

# 1. Richardson Extrapolation

Starting with:

\[
R_{0,0} = T(h_0)
\]

where \( T(h_0) \) is the trapezoid rule with step size \( h_0 = b - a \).

Each refinement halves the step size:

\[
h_k = \frac{b - a}{2^k}
\]

---

# 2. Romberg Table

The first column:

\[
R_{k,0} = \frac{1}{2}R_{k-1,0} + h_k \sum f(\text{midpoints})
\]

Higher-order columns:

\[
R_{k,j} = R_{k,j-1}
+ \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}
\]

The final estimate is:

\[
R_{n,n}
\]

---

# 3. Properties

### Advantages
- Extremely accurate
- Fast convergence for smooth functions
- No need for symbolic derivatives

### Disadvantages
- Requires many function evaluations
- Not ideal for noisy or discontinuous functions

---

# 4. Conceptual Example

For:

\[
f(x) = x^2,\quad [0, 2]
\]

Romberg with depth \( n = 2 \) yields:

\[
R_{2,2} = 2.6666667
\]

matching the exact integral.

---

# End of Document

