
---

# Determinant — Theory

The determinant is a scalar value associated with a square matrix \( A \in \mathbb{R}^{n \times n} \).  
It encodes geometric and algebraic properties of the matrix.

---

# 1. Definition

For a \( 2 \times 2 \) matrix:

\[
A = \begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
\]

\[
\det(A) = ad - bc
\]

For larger matrices, the determinant is defined recursively using cofactor expansion.

---

# 2. Properties

- \( \det(A) = 0 \) ⇔ matrix is singular  
- \( \det(AB) = \det(A)\det(B) \)  
- \( \det(A^{-1}) = 1/\det(A) \)  
- Swapping two rows changes the sign  
- Multiplying a row by \( k \) multiplies determinant by \( k \)

---

# 3. Geometric Interpretation

The determinant represents the **volume scaling factor** of the linear transformation defined by \( A \).

---

# 4. Conceptual Example

\[
A = \begin{pmatrix}
4 & 3 \\
6 & 3
\end{pmatrix}
\]

\[
\det(A) = 4(3) - 3(6) = 12 - 18 = -6
\]

---

# End of Document

---

