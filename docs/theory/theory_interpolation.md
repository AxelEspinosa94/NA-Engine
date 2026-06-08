
---

# 📘 **Theory — Interpolation Methods**

# Numerical Interpolation — Theoretical Foundations

Interpolation is the process of estimating the value of a function at a point where it is not explicitly known, using a set of known data points.  
NA‑Engine supports four classical interpolation techniques:

- Lagrange interpolation  
- Newton divided differences  
- Natural cubic splines  
- Hermite interpolation  

This document provides the mathematical foundations of each method.

---

# 1. Lagrange Interpolation

## 1.1 Overview
Lagrange interpolation constructs a polynomial $P_n(x)$ of degree at most $n$ that passes through all given points:

$$
(x_0, y_0), (x_1, y_1), \dots, (x_n, y_n)
$$

The polynomial is expressed as a linear combination of **Lagrange basis polynomials**.

## 1.2 Lagrange Basis Polynomials

$$
L_i(x) = \prod_{\substack{j=0 \\ j \ne i}}^{n} 
\frac{x - x_j}{x_i - x_j}
$$

## 1.3 Interpolating Polynomial

$$
P_n(x) = \sum_{i=0}^{n} y_i \, L_i(x)
$$

## 1.4 Properties
- Exact for polynomials of degree ≤ $n$
- No need to compute divided differences
- Simple to implement
- Expensive to evaluate repeatedly (recomputes all basis polynomials)

## 1.5 Notes
Lagrange interpolation is best suited for small datasets or one‑off evaluations.

---

# 2. Newton Interpolation (Divided Differences)

## 2.1 Overview
Newton interpolation expresses the polynomial in **Newton form**, which is efficient for incremental construction and evaluation.

## 2.2 Divided Differences

The divided difference table is defined recursively:

$$
f[x_i] = y_i
$$

$$
f[x_i, x_{i+1}] = \frac{f[x_{i+1}] - f[x_i]}{x_{i+1} - x_i}
$$

$$
f[x_i, \dots, x_{i+k}] =
\frac{f[x_{i+1}, \dots, x_{i+k}] - f[x_i, \dots, x_{i+k-1}]}
{x_{i+k} - x_i}
$$

## 2.3 Newton Polynomial

$$
P_n(x) = c_0 
+ c_1(x - x_0)
+ c_2(x - x_0)(x - x_1)
+ \dots
+ c_n(x - x_0)\cdots(x - x_{n-1})
$$

where $c_k = f[x_0, \dots, x_k]$.

## 2.4 Properties
- Efficient for adding new points  
- More numerically stable than Lagrange  
- Reuses previously computed coefficients  

---

# 3. Natural Cubic Splines

## 3.1 Overview
Cubic splines construct a **piecewise cubic polynomial** that is:

- Twice continuously differentiable  
- Interpolates all data points  
- Minimizes curvature  

A *natural spline* additionally satisfies:

$$
S''(x_0) = 0, \quad S''(x_n) = 0
$$

## 3.2 Spline Definition

For each interval \([x_i, x_{i+1}]\):

$$
S_i(x) = 
a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3
$$

Coefficients are determined by solving a tridiagonal system involving second derivatives $M_i = S''(x_i)$.

## 3.3 Tridiagonal System

Let $h_i = x_{i+1} - x_i$.  
For $i = 1, \dots, n-1$:

$$
h_{i-1} M_{i-1} + 2(h_{i-1} + h_i) M_i + h_i M_{i+1}
= 6\left(
\frac{y_{i+1} - y_i}{h_i}
- \frac{y_i - y_{i-1}}{h_{i-1}}
\right)
$$

Boundary conditions:

$$
M_0 = 0, \quad M_n = 0
$$

## 3.4 Evaluation

Once $M_i$ are known, the spline on interval $[x_k, x_{k+1}]$ is:

$$
S(x) =
M_k \frac{(x_{k+1} - x)^3}{6h_k}
+ M_{k+1} \frac{(x - x_k)^3}{6h_k}
+ \left(y_k - \frac{M_k h_k^2}{6}\right)\frac{x_{k+1} - x}{h_k}
+ \left(y_{k+1} - \frac{M_{k+1} h_k^2}{6}\right)\frac{x - x_k}{h_k}
$$

---

# 4. Hermite Interpolation

## 4.1 Overview
Hermite interpolation uses both function values and derivative values:

$$
(x_i, f(x_i), f'(x_i))
$$

It constructs a polynomial that matches:

- Function values  
- First derivatives  

## 4.2 Duplicated Nodes

Hermite interpolation uses a modified Newton form with duplicated nodes:

$$
z_0 = x_0,\; z_1 = x_0,\; z_2 = x_1,\; z_3 = x_1,\; \dots
$$

## 4.3 Divided Differences Matrix $Q$

The first two columns are initialized as:

$$
Q_{2i,0} = f(x_i), \quad Q_{2i+1,0} = f(x_i)
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

Higher-order divided differences:

$$
Q_{i,j} = \frac{Q_{i+1,j-1} - Q_{i,j-1}}{z_{i+j} - z_i}
$$

## 4.4 Hermite Polynomial

$$
H(x) = Q_{0,0}
+ Q_{0,1}(x - z_0)
+ Q_{0,2}(x - z_0)(x - z_1)
+ \dots
$$

## 4.5 Properties
- Matches both values and slopes  
- Produces smoother curves than Lagrange/Newton  
- Useful when derivative information is available  

---

# 5. Summary Table

| Method | Smoothness | Uses Derivatives | Global / Piecewise | Notes |
|-------|------------|------------------|---------------------|-------|
| Lagrange | $C^0$ | No | Global | Simple but expensive |
| Newton | $C^0$ | No | Global | Efficient updates |
| Cubic Spline | $C^2$ | No | Piecewise | Very smooth |
| Hermite | $C^1$ | Yes | Global | Uses slope info |

---

# End of Document

---

