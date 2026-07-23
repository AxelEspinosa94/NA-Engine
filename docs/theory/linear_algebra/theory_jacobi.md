
---

# Jacobi Iteration — Theory

Jacobi solves:

$$
Ax = b
$$

using the iteration:

$$
x_i^{(k+1)} = \frac{1}{A_{ii}}
\left(b_i - \sum_{j\neq i} A_{ij} x_j^{(k)}\right)
$$

---

# 1. Convergence

Converges if:

- $A$ is diagonally dominant  
- Or $A$ is symmetric positive definite  

---

# 2. Conceptual Example

$$
x = (1, 2)
$$

---

# End of Document


