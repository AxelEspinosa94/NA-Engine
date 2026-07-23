

---

### `theory_adams_bashforth.md`

# Adams–Bashforth Methods — Theory

Adams–Bashforth methods are explicit multistep schemes for IVPs:

$$
y' = f(x, y)
$$

They use several past points to predict the next value.

---

## 1. AB2 (Two‑Step)

$$
y_{n+1} = y_n + \frac{h}{2}\left(3 f_n - f_{n-1}\right)
$$

where $f_n = f(x_n, y_n)$.

- Order: 2  
- Requires $y_0, y_1$ (startup via one‑step method like RK2/RK4)

---

## 2. AB3 (Three‑Step)

$$
y_{n+1} = y_n + \frac{h}{12}\left(23 f_n - 16 f_{n-1} + 5 f_{n-2}\right)
$$

- Order: 3  
- Requires $y_0, y_1, y_2$ (startup via RK4, for example)

---

## 3. Properties

- Efficient: reuse past evaluations  
- Explicit: no nonlinear solves per step  
- Stability more delicate than one‑step methods

---

# End of Document
