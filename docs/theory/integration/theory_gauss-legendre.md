
---

# Gauss–Legendre Quadrature — Theory

Gauss–Legendre quadrature is a high‑accuracy numerical integration method that evaluates the integrand at optimally chosen points.

It is exact for all polynomials of degree $\le 2n - 1$.

---

# 1. Legendre Polynomials

The nodes $t_i$ are the roots of the Legendre polynomial $P_n(t)$:

$$
P_n(t_i) = 0
$$

Weights:

$$
w_i = \frac{2}{(1 - t_i^2)[P_n'(t_i)]^2}
$$

---

# 2. Interval Transformation

Legendre nodes are defined on $[-1, 1]$.  
To integrate on $[a, b]$:

$$
x_i = \frac{b - a}{2}t_i + \frac{a + b}{2}
$$

The integral becomes:

$$
\int_a^b f(x)\,dx \approx \frac{b - a}{2} \sum_{i=1}^{n} w_i f(x_i)
$$

---

# 3. Properties

### Advantages
- Very high accuracy
- Requires fewer points than composite rules
- Exact for high‑degree polynomials

### Disadvantages
- Nodes and weights must be computed
- Not ideal for functions with singularities
- More complex than Simpson or trapezoid

---

# 4. Conceptual Example

For:

$$
f(x) = x^2,\quad [0, 2],\quad n = 2
$$

Gauss–Legendre yields:

$$
\approx 2.6666667
$$

matching the exact integral.

---

# End of Document

---

