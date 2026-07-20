
---


# Heun Method (Improved Euler) — Theory

Heun’s method is a predictor–corrector scheme that improves Euler’s method.

---

## 1. Problem

$$
y' = f(x, y), \quad y(x_0) = y_0
$$

---

## 2. Formula

Predictor (Euler):

$$
k_1 = f(x_n, y_n)
$$
$$
y_{\text{pred}} = y_n + h k_1
$$

Corrector:

$$
k_2 = f(x_n + h, y_{\text{pred}})
$$
$$
y_{n+1} = y_n + \frac{h}{2}(k_1 + k_2)
$$

---

## 3. Error and Properties

- Global error: $O(h^2)$ (second‑order method)  
- More accurate than Euler for the same step size  
- Still explicit and easy to implement

---

## 4. Conceptual Example

$$
y' = y,\quad y(0) = 1
$$

Heun averages the slopes at the beginning and end of the interval.

---

# End of Document

