
---

# Matrix Inverse — Theory

The inverse of a square matrix \( A \) is a matrix \( A^{-1} \) such that:

\[
AA^{-1} = A^{-1}A = I
\]

---

# 1. Existence

A matrix is invertible iff:

\[
\det(A) \neq 0
\]

---

# 2. Formula (2×2 case)

\[
A^{-1} = \frac{1}{ad - bc}
\begin{pmatrix}
d & -b \\
-c & a
\end{pmatrix}
\]

---

# 3. Properties

- \( (A^{-1})^{-1} = A \)  
- \( (AB)^{-1} = B^{-1}A^{-1} \)  
- \( (A^T)^{-1} = (A^{-1})^T \)

---

# 4. Conceptual Example

\[
A = \begin{pmatrix}
4 & 3 \\
6 & 3
\end{pmatrix}
\]

\[
A^{-1} = \frac{1}{-6}
\begin{pmatrix}
3 & -3 \\
-6 & 4
\end{pmatrix}
\]

---

# End of Document


