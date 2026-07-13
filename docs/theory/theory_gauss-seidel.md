
---

# Gauss‑Seidel Iteration — Theory

Gauss‑Seidel improves Jacobi by using updated values immediately:

$$
x_i^{(k+1)} = \frac{1}{A_{ii}}
\left(b_i - \sum_{j<i} A_{ij} x_j^{(k+1)} - \sum_{j>i} A_{ij} x_j^{(k)}\right)
$$

---

# 1. Convergence

Faster than Jacobi.  
Converges if:

- $A$ is diagonally dominant  
- Or symmetric positive definite  

---

# 2. Conceptual Example

$$
x = (1, 2)
$$

---

# End of Document

---

