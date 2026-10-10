
---

# Simpson’s Rules — Theory

---

# **Table of Contents**

- [Overview](#overview)
- [Mathematical Foundations](#mathematical-foundations)
  - [Polynomial Interpolation](#polynomial-interpolation)
  - [Quadratic and Cubic Approximations](#quadratic-and-cubic-approximations)
- [Simpson 1/3 Rule](#simpson-13-rule)
- [Simpson 3/8 Rule](#simpson-38-rule)
- [Properties](#properties)
- [Example](#example)
- [Why Simpson’s Rules Matter](#why-simpsons-rules-matter)
- [Sources](#sources)

---

# Overview

Let $f$ be an integrable function over an interval $[a,b]\subset\mathbb{R}$.  
The goal is to approximate:

$$
\int_a^b f(x)\,dx
$$

using polynomial interpolation.

While the trapezoidal rule uses **linear** interpolation, Simpson’s rules use **quadratic** or **cubic** polynomials, achieving significantly higher accuracy.

Both rules belong to the family of **Newton–Cotes formulas**, which approximate integrals using equally spaced nodes.

---

# Mathematical Foundations

## Polynomial Interpolation

Given nodes:

$$
x_0, x_1, x_2, \dots, x_n,
$$

Simpson’s rules approximate $f(x)$ using:

- **Quadratic polynomials** over pairs of intervals (Simpson 1/3)
- **Cubic polynomials** over triplets of intervals (Simpson 3/8)

These interpolating polynomials integrate exactly polynomials of degree:

- ≤ 3 for Simpson 1/3  
- ≤ 3 for Simpson 3/8 (also cubic)

## Quadratic and Cubic Approximations

For a quadratic interpolant:

$$
p_2(x) = ax^2 + bx + c,
$$

the integral over $[x_0,x_2]$ can be computed exactly, giving rise to the 1/3 rule.

For a cubic interpolant:

$$
p_3(x) = ax^3 + bx^2 + cx + d,
$$

integrating over $[x_0,x_3]$ yields the 3/8 rule.

---

# Simpson 1/3 Rule

Requires an **even** number of subintervals $n$.

Let:

$$
h = \frac{b-a}{n}.
$$

Then:

$$
S = \frac{h}{3}
\left[
f(x_0) + f(x_n)
+ 4\sum_{\text{odd } i} f(x_i)
+ 2\sum_{\text{even } i} f(x_i)
\right].
$$

Interpretation:

- Odd-indexed nodes → weight 4  
- Even-indexed interior nodes → weight 2  
- Endpoints → weight 1  

This corresponds to fitting parabolas over pairs of intervals.

---

# Simpson 3/8 Rule

Requires $n$ to be a **multiple of 3**.

$$
S = \frac{3h}{8}
\left[
f(x_0) + f(x_n)
+ 3\sum_{i\not\equiv 0\pmod{3}} f(x_i)
+ 2\sum_{i\equiv 0\pmod{3}} f(x_i)
\right].
$$

Interpretation:

- Nodes not divisible by 3 → weight 3  
- Nodes divisible by 3 (interior) → weight 2  
- Endpoints → weight 1  

This rule fits cubic polynomials over groups of three intervals.

---

# Properties

### Advantages
- High accuracy: global error $O(h^4)$  
- Excellent for smooth functions  
- Composite versions are efficient  
- Often dramatically more accurate than trapezoid  

### Disadvantages
- Requires specific constraints on $n$  
- Not ideal for discontinuous or highly oscillatory functions  
- Uses equally spaced nodes (less optimal than Gaussian quadrature)

---

# Example

Consider:

$$
f(x)=x^2,\quad [0,2],\quad n=6.
$$

### Analytical value

$$
\int_0^2 x^2\,dx = \frac{8}{3} \approx 2.6666667.
$$

### Simpson 1/3 Rule

|i|$x_{i}$|$f(x_{i})$|
|-|-------|----------|
|0|$0$|$0$|
|1|$1/3$|$1/9$|
|2|$2/3$|$2/9$|
|3|$1$|$1$|
|4|$4/3$|$16/9$|
|5|$5/3$|$25/9$|
|6|$2$|$4$|


$h=\frac{2}{6}=\frac{1}{3}$

$$
\begin{align}
S = \frac{h}{3}\left[f(x_0) + f(x_n)+ 4\sum_{\text{odd } i} f(x_i)+ 2\sum_{\text{even } i} f(x_i)\right]  \\
= \frac{\frac{1}{3}}{3}\left[0 + 4 + 4\left(\frac{1}{9}+1+\frac{25}{9}\right)+ 2\left(\frac{2}{9}+\frac{16}{9}\right)\right]  \\
= \frac{1}{9}\left[4 + 4\left(\frac{35}{9}\right)+ 2\left(2\right)\right]  \\
= \frac{1}{9}\left[\frac{212}{9}\right]  \\
\approx 2.6173
\end{align}
$$

which minimizes the error seen in the trapezoid calculations

### Simpson 3/8 Rule

$$
\begin{align}
S = \frac{3h}{8}\left[f(x_0) + f(x_n)+ 3\sum_{i\not\equiv 0\pmod{3}} f(x_i)+ 2\sum_{i\equiv 0\pmod{3}} f(x_i)\right]  \\
= \frac{3\frac{1}{3}}{8}\left[0 + 4 + 3\left(\frac{1}{9}+\frac{2}{9}+\frac{16}{9}+\frac{25}{9}\right)+ 2\right]  \\
= \frac{1}{8}\left[4 + 3\left(\frac{44}{9}\right)+ 2\right]  \\
= \frac{1}{8}\left[4 + 3\left(\frac{44}{9}\right)+ 2\right]  \\
\approx 2.5833
\end{align}
$$

Which doesn't improve the calculation from the 1/3 rule perse. This has an explanation and it is evident by looking the calculation. Simpson 3/8 rule relay in the suposition that $n$ is big enough so the nodes are proportionally distributed. In this case we only have a single node which index is divisible with 3 vs four nodes which index isn't.

---

# Why Simpson’s Rules Matter

Simpson’s rules are foundational in numerical analysis:

### ✔ They provide high accuracy with minimal complexity  
Quadratic and cubic interpolation capture curvature far better than linear methods.

### ✔ They are the backbone of many composite integration schemes  
Romberg integration uses trapezoid, but Simpson is often preferred for standalone composite rules.

### ✔ They are ideal for smooth functions  
Especially when the integrand behaves like a low-degree polynomial.

### ✔ They are widely used in engineering and physics  
Particularly when data is evenly spaced.

---

# Sources

- Burden, R. L., & Faires, J. D. (2001). Numerical Analysis (7th ed., pp. 190-193). Brooks/Cole.

---
