
---

# Trapezoidal Rule — Theory

---

# **Table of Contents**

- [Overview](#overview)
- [Mathematical Foundations](#mathematical-foundations)
  - [Geometric Interpretation](#geometric-interpretation)
  - [Partition and Subintervals](#partition-and-subintervals)
- [Simple Trapezoid Rule](#simple-trapezoid-rule)
- [Composite Trapezoid Rule](#composite-trapezoid-rule)
- [Properties](#properties)
- [Worked Example](#worked-example)
- [Why the Trapezoid Rule Matters](#why-the-trapezoid-rule-matters)
- [Sources](#sources)

---

# Overview

Let $ f $ be an integrable function over an interval $[a,b]\subset\mathbb{R}$.  
The goal is to approximate:

$$
\int_a^b f(x)\,dx
$$

using a numerical method based on **linear interpolation**.

Classical Riemann sums satisfy:

$$
L(f,P) \le \int_a^b f(x)\,dx \le U(f,P),
$$

but their convergence is slow.  
The **Trapezoidal Rule** improves this by replacing rectangles with **trapezoids**, yielding a better approximation with minimal additional cost.

---

# Mathematical Foundations

## Geometric Interpretation

The trapezoidal rule approximates the graph of $f(x)$ on each subinterval by a **straight line** connecting the endpoints:

$$
(x_i, f(x_i)) \quad \text{and} \quad (x_{i+1}, f(x_{i+1})).
$$

The area under this line segment forms a trapezoid.

## Partition and Subintervals

Given a partition:

$$
a = x_0 < x_1 < \cdots < x_n = b,
$$

with uniform spacing:

$$
h = \frac{b-a}{n},
$$

the integral is approximated by summing the areas of the trapezoids.

---

# Simple Trapezoid Rule

The simplest case uses **one single trapezoid** over $[a,b]$:

$$
T = \frac{b-a}{2}\left[f(a) + f(b)\right].
$$

This corresponds to approximating the entire interval with a single linear segment.

---

# Composite Trapezoid Rule

For $n$ subintervals of equal width:

$$
h = \frac{b-a}{n},
$$

the composite rule is:

$$
T = h\left[\frac{f(x_0)}{2} + \sum_{i=1}^{n-1} f(x_i) + \frac{f(x_n)}{2}\right]
$$

Each interior point contributes fully, while endpoints contribute half, reflecting the geometry of trapezoids.

---

# Properties

### Advantages
- Extremely simple to implement  
- Works for any continuous function  
- Good coarse approximation  
- Forms the basis for more advanced methods (Simpson, Romberg)

### Disadvantages
- Low accuracy: global error $O(h^2)$  
- Requires many subintervals for high precision  
- Sensitive to curvature (linear approximation only)

---

# Worked Example

Consider:

$$
f(x)=x^2,\quad [0,2].
$$

### Analytical value

$$
\int_0^2 x^2\,dx = \frac{8}{3} \approx 2.6666667.
$$

### Simple Trapezoid

$$
T = \frac{2}{2}(0^2 + 2^2) = 4.
$$

The trapezoid rule **overestimates** the true value because $x^2$ is convex.

### Composite Trapezoid

Let $n=4$, $h=\frac{2-0}{4}=\frac{2}{4}=\frac{1}{2}$

|i|$x_{i}$|$f(x_{i})$|
|-|-------|----------|
|0|$0$|$0$|
|1|$1/2$|$1/4$|
|2|$1$|$1$|
|3|$3/2$|$9/4$|
|4|$2$|$4$|

$$
\begin{align}
T = h\left[\frac{f(x_0)}{2} + \sum_{i=1}^{3} f(x_i) + \frac{f(x_4)}{2}\right] \\
= \frac{1}{2}\left[\frac{0^{2}}{2} + \sum_{i=1}^{n-1} f(x_i) + \frac{2^{2}}{2}\right] \\
= \frac{1}{2}\left[0 + \sum_{i=1}^{n-1} f(x_i) + 2\right] \\
= \frac{1}{2}\left[0 + \frac{1}{4} + 1 +\frac{9}{4} + 2\right] \\
= \frac{1}{2}\left[\frac{11}{2}\right]  \\
= \frac{11}{4}\approx 2.75
\end{align}
$$

Which is a better estimation compared to the Simple Trapezoid calculation.

---

# Why the Trapezoid Rule Matters

Even though it is simple, the trapezoid rule is foundational:

### ✔ It is the building block of Simpson’s Rule  
Simpson’s Rule is essentially a correction of the trapezoid rule using quadratic interpolation.

### ✔ It is the first column of Romberg Integration  
Romberg extrapolates trapezoid approximations to achieve high precision.

### ✔ It is robust and general  
Works for any continuous function without special requirements.

### ✔ It is widely used in engineering  
Especially when data comes from measurements rather than analytic functions.

---

# Sources

- Burden, R. L., & Faires, J. D. (2001). Numerical Analysis (7th ed., pp. 188). Brooks/Cole.

---

