
---


```markdown
# Runge–Kutta 2 (Midpoint) — Theory

RK2 (midpoint method) is a second‑order Runge–Kutta scheme.

---

## 1. Problem

\[
y' = f(x, y), \quad y(x_0) = y_0
\]

---

## 2. Formula

\[
k_1 = f(x_n, y_n)
\]
\[
k_2 = f\left(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1\right)
\]
\[
y_{n+1} = y_n + h k_2
\]

---

## 3. Error and Properties

- Global error: \( O(h^2) \)  
- Uses slope at the midpoint for better accuracy  
- Good compromise between cost and precision

---

## 4. Conceptual Example

\[
y' = y,\quad y(0) = 1
\]

RK2 uses the slope at \( x_n + h/2 \) instead of at \( x_n \) or \( x_n + h \).

---

# End of Document
```

