
---

# Natural Cubic Spline Interpolation — Theory

Cubic splines construct a smooth, piecewise cubic function that interpolates all data points and has continuous first and second derivatives.

---

# 1. Spline Definition

For each interval \([x_i, x_{i+1}]\):

$$
S_i(x) =
a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3
$$

The coefficients are determined using:

- Interpolation conditions
- Continuity of $S$, $S'$, and $S''$
- Boundary conditions

---

# 2. Natural Boundary Conditions

A natural spline satisfies:

$$
S''(x_0) = 0,\quad S''(x_n) = 0
$$

This minimizes curvature.

---

# 3. Tridiagonal System for Second Derivatives

Let $h_i = x_{i+1} - x_i$.  
For $i = 1, \dots, n-1$:

$$
h_{i-1} M_{i-1}+ 2(h_{i-1} + h_i) M_i+ h_i M_{i+1}=6\left(\frac{y_{i+1} - y_i}{h_i}- \frac{y_i - y_{i-1}}{h_{i-1}}\right)
$$

Boundary:

$$
M_0 = 0,\quad M_n = 0
$$

---

# 4. Evaluation Formula

For $x \in [x_k, x_{k+1}]$:

$$
S(x) =M_k \frac{(x_{k+1} - x)^3}{6h_k}+ M_{k+1} \frac{(x - x_k)^3}{6h_k}+ \left(y_k - \frac{M_k h_k^2}{6}\right)\frac{x_{k+1} - x}{h_k}+ \left(y_{k+1} - \frac{M_{k+1} h_k^2}{6}\right)\frac{x - x_k}{h_k}
$$

---

# 5. Properties

### Advantages
- Very smooth ($C^2$)
- Piecewise local behavior
- No Runge phenomenon

### Disadvantages
- Requires solving a linear system
- More complex than Lagrange/Newton

---

# 6. Conceptual Example

Given:

$$
(0, 1),\ (1, 2),\ (2, 5)
$$

The spline yields a smooth curve passing through all points.  
Evaluating at $x = 1$ gives:

$$
S(1) = 2
$$

---

# End of Document

---

