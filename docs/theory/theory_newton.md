
---

# Newton Interpolation — Theory

Newton interpolation expresses the interpolating polynomial in a form that is efficient to compute and update.

---

# 1. Divided Differences

The divided difference table is defined recursively.

### Zeroth order:
$$
f[x_i] = y_i
$$

### First order:
$$
f[x_i, x_{i+1}] = \frac{f[x_{i+1}] - f[x_i]}{x_{i+1} - x_i}
$$

### Higher order:
$$
f[x_i, \dots, x_{i+k}] =
\frac{f[x_{i+1}, \dots, x_{i+k}] - f[x_i, \dots, x_{i+k-1}]}
{x_{i+k} - x_i}
$$

The first element of each column becomes a coefficient.

---

# 2. Newton Polynomial

$$
P_n(x) = c_0 + c_1(x - x_0)+ c_2(x - x_0)(x - x_1)+ \dots+ c_n(x - x_0)\cdots(x - x_{n-1})
$$

where:

$$
c_k = f[x_0, \dots, x_k]
$$

---

# 3. Properties

### Advantages
- Efficient for incremental updates
- More numerically stable than Lagrange
- Reuses previously computed coefficients

### Disadvantages
- Still a global polynomial
- Requires divided difference table

---

# 4. Conceptual Example

Given:

$$
(0, 1),\ (1, 2),\ (2, 5)
$$

The divided differences yield:

$$
c_0 = 1,\quad c_1 = 1,\quad c_2 = 1
$$

Thus:

$$
P(x) = 1 + 1(x - 0) + 1(x - 0)(x - 1)
$$

Evaluating at \( x = 1$:

$$
P(1) = 2
$$

---

# End of Document

---
