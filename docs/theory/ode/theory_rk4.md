
---

### `theory_rk4.md`

# Runge–Kutta 4 (RK4) — Theory

RK4 is the classical fourth‑order Runge–Kutta method, widely used for IVPs.

---

## 1. Problem

$$
y' = f(x, y), \quad y(x_0) = y_0
$$

---

## 2. Formula

$$
\begin{aligned}
k_1 &= f(x_n, y_n) \\
k_2 &= f\left(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1\right) \\
k_3 &= f\left(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_2\right) \\
k_4 &= f(x_n + h, y_n + h k_3) \\
y_{n+1} &= y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)
\end{aligned}
$$

---

## 3. Error and Properties

- Global error: $O(h^4)$  
- Very accurate for moderate step sizes  
- Workhorse method in many applications

---

## 4. Conceptual Example

$$
y' = y,\quad y(0) = 1
$$

RK4 approximates $e^x$ very accurately even with relatively large $h$.

---

# End of Document

