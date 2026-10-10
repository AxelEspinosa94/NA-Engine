
---

# Monte Carlo Integration — Theory 

---

# **Table of Contents**

- [Overview](#overview)
- [Mathematical Foundations](#mathematical-foundations)
  - [Random Sampling](#random-sampling)
  - [Expectation Interpretation](#expectation-interpretation)
- [Monte Carlo Integration](#monte-carlo-integration)
  - [Uniform Sampling](#uniform-sampling)
  - [General Formula](#general-monte-carlo-estimator-nd)
- [Variance and Error](#variance-and-error)
- [Properties](#properties)
- [Example](#worked-example)
- [Why Monte Carlo Is Powerful](#why-monte-carlo-is-powerful)
- [Sources](#sources)

---

# Overview

Monte Carlo integration is a **numerical method** that estimates integrals using **random sampling**. Unlike deterministic quadrature rules (Simpson, Gauss, Romberg), Monte Carlo does not rely on polynomial interpolation or fixed nodes. Instead, it approximates:

$$
\int_a^b f(x),dx
$$

by evaluating $f$ at randomly chosen points inside the interval.

Monte Carlo is especially useful when:

- the integrand is irregular or high‑dimensional,  
- deterministic quadrature becomes expensive,  
- only stochastic sampling is available (e.g., physics simulations).

---

# Mathematical Foundations

## Random Sampling

Let $X$ be a random variable uniformly distributed on $[a,b]$:

$$
X \sim U(a,b).
$$

Then:

$$
\mathbb{E}[f(X)] = \frac{1}{b-a}\int_a^b f(x)\,dx.
$$

This identity is the foundation of Monte Carlo integration.

## Expectation Interpretation

Rearranging:

$$
\int_a^b f(x)\,dx = (b-a)\,\mathbb{E}[f(X)].
$$

Monte Carlo approximates the expectation by averaging samples:

$$
\mathbb{E}[f(X)] \approx \frac{1}{N}\sum_{i=1}^N f(X_i),
$$

where each $X_i$ is an independent uniform sample.

---

# Monte Carlo Integration

## ND Uniform Sampling

Monte Carlo integration estimates an integral by averaging random evaluations of the integrand inside the domain. This generalized formulation works for any dimension $d \ge 1$.

---

## Multidimensional Domain

Let $D \subset \mathbb{R}^d$ be a domain with **volume**:

$$
V = \int_D 1 \, dV.
$$

For a hyper-rectangular domain:

$$
D = [a_1,b_1] \times [a_2,b_2] \times \dots \times [a_d,b_d],
$$

the volume is:

$$
V = \prod_{j=1}^d (b_j - a_j).
$$

---

## Uniform Sampling

Generate $N$ random points:

$$
X_i \sim U(D), \quad i = 1,\dots,N,
$$

where $U(D)$ denotes the uniform distribution over the domain.

Evaluate the integrand:

$$
f(X_1), f(X_2), \dots, f(X_N).
$$

---

## General Monte Carlo Estimator (ND)

For the integral:

$$
I = \int_D f(x)\, dV,
$$

the Monte Carlo estimator is:

$$
\boxed{
I_N = V \cdot \frac{1}{N} \sum_{i=1}^N f(X_i)
}
$$

By the **Law of Large Numbers**:

$$
I_N \xrightarrow[]{N\to\infty} I.
$$

---

## Special Cases

### 1D Case

Domain:

$$
D = [a,b], \qquad V = b-a.
$$

Estimator:

$$
I_N = (b-a)\frac{1}{N}\sum_{i=1}^N f(X_i), \quad X_i \sim U(a,b).
$$

---

### 2D Case

Rectangular domain:

$$
D = [a_1,b_1] \times [a_2,b_2], \qquad V = (b_1-a_1)(b_2-a_2).
$$

Estimator:

$$
I_N = (b_1-a_1)(b_2-a_2)\frac{1}{N}\sum_{i=1}^N f(X_i, Y_i).
$$

---

### ND Case

Hyper-rectangular domain:

$$
D = \prod_{j=1}^d [a_j,b_j], \qquad V = \prod_{j=1}^d (b_j-a_j).
$$

Estimator:

$$
I_N = \left( \prod_{j=1}^d (b_j-a_j) \right)
\frac{1}{N}\sum_{i=1}^N f(X_i).
$$

---

## Classical Formula (Press et al., 1992)

$$
\int_D f\, dV \approx
V\langle f\rangle
\pm
V\sqrt{\frac{\langle f^2\rangle - \langle f\rangle^2}{N}},
$$

where:

$$
\langle f\rangle = \frac{1}{N}\sum_{i=1}^N f(X_i), \qquad
\langle f^2\rangle = \frac{1}{N}\sum_{i=1}^N f(X_i)^2.
$$

---

# Variance and Error

Monte Carlo error behaves differently from deterministic quadrature.

The standard deviation of the estimator is:

$$
\sigma_N = (b-a)\frac{\sigma_f}{\sqrt{N}},
$$

where:

$$
\sigma_f^2 = \mathbb{V}[f(X)].
$$

Thus:

### ✔ Error decays as $O(N^{-1/2})$

This is slower than Simpson ($O(h^4)$) or Romberg (super‑convergent), but **dimension‑independent**, making Monte Carlo ideal for high‑dimensional integrals.

---

# Properties

### Advantages
- Works for irregular, noisy, or discontinuous functions  
- Dimension‑independent convergence  
- Easy to implement  
- Parallelizable (samples are independent)  
- Useful when only random samples are available  

### Disadvantages
- Slow convergence: $O(N^{-1/2})$  
- Requires many samples for high precision  
- Results are stochastic (vary run to run)  

---

# Example

Consider:

$$
f(x)=x^2,\quad [0,2].
$$

The exact integral is:

$$
I = \frac{8}{3} \approx 2.6666667.
$$

We generate $N=5$ random uniform samples in $[0,2]$.  
Suppose the samples are:

$$
X = {0.12, 0.77, 1.31, 1.88, 0.55}.
$$

Evaluate:

| $X_i$ | $f(X_i)=X_i^2$ |
|--------|------------------|
| 0.12   | 0.0144           |
| 0.77   | 0.5929           |
| 1.31   | 1.7161           |
| 1.88   | 3.5344           |
| 0.55   | 0.3025           |

Compute the average:

$$
\frac{1}{5}(0.0144 + 0.5929 + 1.7161 + 3.5344 + 0.3025)
= \frac{6.1603}{5}
= 1.23206.
$$

Multiply by interval length:

$$
I_5 = 2 \cdot 1.23206 = 2.46412.
$$

Relative Error:

$$
|2.46412 - 2.6666667| \approx 0.2025.
$$

With more samples, the estimate improves:

| Samples $N$ | Estimate $I_N$ | Error |
|---------------|------------------|-------|
| 5             | 2.46             | 0.20  |
| 50            | 2.63             | 0.03  |
| 500           | 2.668            | 0.001 |
| 5000          | 2.6668           | 0.0001 |

Monte Carlo converges slowly but steadily.

---

# Why Monte Carlo Is Powerful

Monte Carlo shines in scenarios where deterministic quadrature fails:

### ✔ High‑dimensional integrals  
Simpson, Gauss, and Romberg explode in cost as dimension grows.  
Monte Carlo does **not**.

### ✔ Irregular or noisy functions  
Monte Carlo does not require smoothness.

### ✔ Probabilistic models  
Physics, finance, and machine learning often produce random samples directly.

### ✔ Parallel computing  
Each sample is independent → trivial parallelization.

Monte Carlo is foundational in:

- statistical physics  
- Bayesian inference  
- rendering (path tracing)  
- stochastic differential equations  
- machine learning  

---

# Sources

- Press, W. H. et. al. (1992) "Simple Monte Carlo Integration" and "Adaptive and Recursive Monte Carlo Methods." §7.6 and 7.8 in Numerical Recipes in FORTRAN: The Art of Scientific Computing, 2nd ed. Cambridge, England: Cambridge University Press, pp. 295-299 and 306-319, 1992.
- Hammersley, J. M. (1960) "Monte Carlo Methods for Solving Multivariable Problems." Ann. New York Acad. Sci. 86, 844-874.

---
