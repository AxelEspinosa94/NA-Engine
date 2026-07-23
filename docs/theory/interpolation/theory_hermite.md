
---

# Hermite Interpolation — Theory

Hermite interpolation uses both function values and derivative values at each node:

$$
(x_i, f(x_i), f'(x_i))
$$

It constructs a polynomial that matches both values and slopes.

---

# 1. Duplicated Nodes

Hermite interpolation uses a modified Newton form with duplicated nodes:

$$
z_0 = x_0,\; z_1 = x_0,\; z_2 = x_1,\; z_3 = x_1,\; \dots
$$

---

# 2. Divided Differences Matrix $Q$

Initialization:

$$
Q_{2i,0} = f(x_i),\quad Q_{2i+1,0} = f(x_i)
$$

$$
Q_{2i,1} = f'(x_i)
$$

$$
Q_{2i+1,1} =
\begin{cases}
f'(x_i), & i = n-1 \\
\dfrac{f(x_{i+1}) - f(x_i)}{x_{i+1} - x_i}, & \text{otherwise}
\end{cases}
$$

Higher-order:

$$
Q_{i,j} = \frac{Q_{i+1,j-1} - Q_{i,j-1}}{z_{i+j} - z_i}
$$

---

# 3. Hermite Polynomial

$$
H(x) =Q_{0,0}+ Q_{0,1}(x - z_0)+ Q_{0,2}(x - z_0)(x - z_1)+ \dots
$$

---

# 4. Properties

### Advantages
- Matches both values and slopes
- Produces smoother curves than Lagrange/Newton
- Useful when derivative information is available

### Disadvantages
- Requires derivative data or symbolic differentiation
- More computationally expensive

---

# 5. Conceptual Example

Given:

$$
(0, 1, 0),\ (1, 2, 1)
$$

The Hermite polynomial evaluates to:

$$
H(0.5) \approx 1.375
$$

---

# End of Document

---

