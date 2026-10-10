
---

# Romberg Integration — Theory

---

# **Table of Contents**

- [Overview](#overview)
- [Mathematical Foundations](#mathematical-foundations)
  - [Trapezoid Refinement](#trapezoid-refinement)
  - [Richardson Extrapolation](#richardson-extrapolation)
- [Romberg Table](#romberg-table)
- [Quadrature Rule](#quadrature-rule)
- [Properties](#properties)
- [Example](#example)
- [Why Romberg Integration Is Powerful](#why-romberg-integration-is-powerful)
- [Sources](#sources)

---

# Overview

Let $f$ be an integrable function over an interval $[a,b]\subset\mathbb{R}$.  
The goal is to approximate:

$$
\int_a^b f(x)\,dx
$$

with **very high accuracy**, using only evaluations of $f$.

Romberg integration achieves this by:

1. Applying the **trapezoid rule** with progressively smaller step sizes.
2. Using **Richardson extrapolation** to eliminate error terms.
3. Building a triangular table of increasingly accurate estimates.

Romberg is one of the most powerful deterministic integration methods for smooth functions.

---

# Mathematical Foundations

## Trapezoid Refinement

Romberg begins with the trapezoid rule:

$$
T(h_0),\quad h_0 = b - a.
$$

Each refinement halves the step size:

$$
h_k = \frac{b-a}{2^k}.
$$

This generates a sequence of trapezoid approximations:

$$
R_{k,0} = T(h_k).
$$

These values converge to the true integral with order $O(h^2)$.

## Richardson Extrapolation

Richardson extrapolation accelerates convergence by eliminating leading error terms.

Given two approximations:

$$
R_{k,0},\quad R_{k-1,0},
$$

the extrapolated value is:

$$
R_{k,1} = R_{k,0} + \frac{R_{k,0} - R_{k-1,0}}{4 - 1}.
$$

Higher-order extrapolations follow:

$$
R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}.
$$

This removes error terms of order $h^2, h^4, h^6,\dots$.

---

# Romberg Table

Romberg constructs a triangular table:

$$
\begin{matrix}
R_{0,0} \\
R_{1,0} & R_{1,1} \\
R_{2,0} & R_{2,1} & R_{2,2} \\
\vdots & \vdots & \vdots & \ddots
\end{matrix}
$$

Where:

- Column 0 → trapezoid approximations  
- Column 1 → first extrapolation  
- Column 2 → second extrapolation  
- …  
- Column $n$ → highest accuracy  

The final estimate is:

$$
R_{n,n}.
$$

---

# Quadrature Rule

### First Column (Trapezoid Refinement)

$$
R_{k,0} = \frac{1}{2}R_{k-1,0} + h_k \sum f(\text{midpoints}).
$$

### Higher Columns (Richardson Extrapolation)

$$
R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}.
$$

Romberg achieves extremely fast convergence—often reaching machine precision with few levels.

---

# Properties

### Advantages
- Extremely accurate  
- Fast convergence for smooth functions  
- No derivatives required  
- Builds on trapezoid rule (simple foundation)

### Disadvantages
- Requires many function evaluations  
- Not suitable for noisy or discontinuous functions  
- Memory grows with table size  

---

# Example

Consider:

$$
f(x)=x^2,\quad [0,2],\quad n=2.
$$

### Analytical value

$$
\int_0^2 x^2\,dx = \frac{8}{3} \approx 2.6666667.
$$

### Romberg Table (Depth 2)

**1.** $R_{0,0}$: trapezoid with $h_0 = 2$  

We use a single trapezoid:

$$
R_{0,0}=T(h_{0})=\frac{2}{2}(f(0)+f(2))=4
$$

which results in an absolute error of $1.33$.

**2.** $R_{1,0}$: trapezoid with $h_1 = 1$  

Now we divide in 2 subintervals $x= 0, 1, 2$

$$
R_{1,0}=T(h_{1})=1\left(\frac{0}{2}+1+\frac{4}{2}\right)=3
$$

which improves the absolute error, but it is still far.

**3.** $R_{2,0}$: trapezoid with $h_2 = 1/2$

Now we divide in $4$ subintervals $x= 0, 0.5, 1, 1.5, 2$

$$
R_{2,0}=T(h_{2})=\frac{1}{2}\left(0+\frac{1}{4}+1+\frac{9}{4}+2\right)=2.75
$$

Which is even better, but still not the value we are looking for.


Then apply Richardson extrapolation with the formula:

$$
R_{k,1} = R_{k,0}+\frac{R_{k,0}-R_{k-1,0}}{4-1}
$$

Then we reach the first level of the extrapolation

$$
\begin{align}
R_{1,1} = R_{1,0}+\frac{R_{1,0}-R_{0,0}}{4-1}   \\
= 3 +\frac{3-4}{3}  \\
=\frac{2}{3}\approx 2.666667
\end{align}
$$

which matches the value calculated analytically.

We can get the second level:

$$
\begin{align}
R_{2,1} = R_{2,0}+\frac{R_{2,0}-R_{1,0}}{4-1}   \\
= 2.75 +\frac{2.75-3}{3}  \\
=2.75 - \frac{0.25}{3}\approx 2.666667
\end{align}
$$

which again matches the analytical result.

And finally we reach the third level of Richardson extrapolation:

$$
\begin{align}
R_{2,2} = R_{2,1}+\frac{R_{2,1}-R_{1,1}}{4^{2}-1}   \\
= 2.666667 +\frac{2.666667-2.666667}{15}  \\
= 2.666667 - 0\approx 2.666667
\end{align}
$$

which means there was nothing else to extrapolate since the column was already exact.

Final result:

$$
R_{2,2} = 2.6666667,
$$

which matches the exact integral.

---

# Why Romberg Integration Is Powerful

Romberg’s strength lies in its **error cancellation**:

### ✔ Richardson extrapolation eliminates error terms  
Each column removes higher-order error components.

### ✔ Convergence is extremely fast  
Often exponential in practice.

### ✔ Uses only trapezoid rule evaluations  
No need for symbolic derivatives or special nodes.

### ✔ Ideal for smooth integrands  
Especially when high precision is required.

Romberg is widely used in:

- scientific computing  
- physics simulations  
- engineering analysis  
- high‑precision numerical integration  

---

# Sources

- Burden, R. L., & Faires, J. D. (2001). Numerical Analysis (7th ed., pp. 207-211). Brooks/Cole.

---
