
---


# Shooting Method for BVPs — Theory

The shooting method converts a boundary value problem (BVP) into an initial value problem (IVP).

---

## 1. Problem

Second‑order BVP:

$$
y'' = f(x, y), \quad y(x_0) = \alpha,\quad y(x_1) = \beta
$$

---

## 2. Idea

Introduce:

$$
y_1 = y,\quad y_2 = y'
$$

Then:

$$
\begin{cases}
y_1' = y_2 \\
y_2' = f(x, y_1)
\end{cases}
$$

Choose an initial slope $s = y'(x_0)$, solve IVP:

$$
y_1(x_0) = \alpha,\quad y_2(x_0) = s
$$

Adjust $s$ so that $y_1(x_1; s) \approx \beta$.

---

## 3. Newton Iteration on s

Define:

$$
\Phi(s) = y_1(x_1; s) - \beta
$$

We want $\Phi(s) = 0$. Newton’s method:

$$
s_{k+1} = s_k - \frac{\Phi(s_k)}{\Phi'(s_k)}
$$

\(\Phi'(s)\) is approximated numerically by integrating with $s$ and $s + \varepsilon$.

---

## 4. Properties

- Uses IVP solvers (e.g., RK4)  
- Can fail for strongly nonlinear or unstable problems  
- Intuitive: “shoot” from one boundary to hit the other

---

# End of Document

