
---

# Lagrange Interpolation — Theory

Lagrange interpolation constructs a polynomial of degree at most \( n \) that passes through all given data points:

\[
(x_0, y_0), (x_1, y_1), \dots, (x_n, y_n)
\]

It is one of the simplest and most direct interpolation techniques.

---

## 1. Lagrange Basis Polynomials

For each index \( i \), the Lagrange basis polynomial is:

\[
L_i(x) = \prod_{\substack{j=0 \\ j \ne i}}^{n}
\frac{x - x_j}{x_i - x_j}
\]

Each \( L_i(x) \) satisfies:

\[
L_i(x_j) = 
\begin{cases}
1 & j = i \\
0 & j \ne i
\end{cases}
\]

---

## 2. Interpolating Polynomial

The interpolating polynomial is:

\[
P_n(x) = \sum_{i=0}^{n} y_i \, L_i(x)
\]

This guarantees:

\[
P_n(x_i) = y_i
\]

---

## 3. Properties

### Advantages
- Simple and intuitive
- No need to compute divided differences
- Exact for polynomials of degree ≤ \( n \)

### Disadvantages
- Computationally expensive for repeated evaluations
- Sensitive to large \( n \) (Runge phenomenon)
- Global polynomial: changing one point affects the entire curve

---

## 4. Conceptual Example

Given:

\[
(0, 1),\ (1, 2),\ (2, 5)
\]

The Lagrange polynomial is:

\[
P(x) = 1 \cdot L_0(x) + 2 \cdot L_1(x) + 5 \cdot L_2(x)
\]

Evaluating at \( x = 1 \):

\[
P(1) = 2
\]

---

# End of Document

---