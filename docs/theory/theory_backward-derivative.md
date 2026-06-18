
---


```markdown
# Backward Difference — Theory

Backward difference approximates the first derivative using a point behind \( x \):

\[
f'(x) \approx \frac{f(x) - f(x-h)}{h}
\]

---

## 1. Formula

\[
D_f^{-}(x) = \frac{f(x) - f(x-h)}{h}
\]

---

## 2. Error

For smooth \( f \):

\[
f'(x) = D_f^{-}(x) + \frac{h}{2}f''(x) + O(h^2)
\]

Also **first‑order accurate**.

---

## 3. Properties

- Useful when values ahead of \( x \) are not available  
- Same accuracy as forward difference  
- Less accurate than central difference  

---

## 4. Conceptual Example

For:

\[
f(x) = \sin(x),\quad x = 1,\quad h = 10^{-4}
\]

\[
f'(1) \approx \frac{\sin(1) - \sin(1 - h)}{h}
\]

---

# End of Document
```

---

