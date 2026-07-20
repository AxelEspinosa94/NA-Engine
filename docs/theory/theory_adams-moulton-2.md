
---

# Adams–Moulton 2 (Trapezoidal Rule) — Theory

Adams–Moulton methods are implicit multistep schemes.  
The 2‑step version is closely related to the trapezoidal rule.

---

## 1. AM2 Formula

$$
y_{n+1} = y_n + \frac{h}{12}\left(5 f_{n+1} + 8 f_n - f_{n-1}\right)
$$

where $f_{n+1} = f(x_{n+1}, y_{n+1})$ depends on the unknown $y_{n+1}$.

---

## 2. Predictor–Corrector

To avoid solving a nonlinear equation exactly, a predictor–corrector scheme is used:

1. Predictor (e.g., AB2):

$$
y_{\text{pred}} = y_n + \frac{h}{2}(3 f_n - f_{n-1})
$$

2. Corrector (AM2):

$$
y_{n+1} \approx y_n + \frac{h}{12}\left(5 f(x_{n+1}, y_{\text{pred}}) + 8 f_n - f_{n-1}\right)
$$

Optionally iterate the corrector for more accuracy.

---

## 3. Properties

- Higher accuracy and better stability than explicit AB methods  
- Implicit nature improves behavior on stiff problems  
- Requires at least one predictor step

---

# End of Document

---
