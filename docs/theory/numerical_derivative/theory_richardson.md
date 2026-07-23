
---


# Richardson Extrapolation — Theory

Richardson extrapolation improves a low‑order approximation by combining estimates at different step sizes.

Applied to central difference:

$$
D(h) = \frac{f(x+h) - f(x-h)}{2h}
$$

$$
D(2h) = \frac{f(x+2h) - f(x-2h)}{4h}
$$

---

## 1. Extrapolation Formula

For order $p$:

$$
D_{\text{rich}} = D(h) + \frac{D(h) - D(2h)}{2^p - 1}
$$

This cancels leading error terms and increases accuracy.

---

## 2. Properties

- Boosts accuracy without symbolic derivatives  
- Sensitive to round‑off for very small $h$  
- Commonly used with $p = 2$  

---

## 3. Conceptual Example

For:

$$
f(x) = \sin(x),\quad x = 1,\quad h = 10^{-3},\quad p = 2
$$

Richardson extrapolation refines the central difference estimate of $f'(1)$.

---

# End of Document
```

