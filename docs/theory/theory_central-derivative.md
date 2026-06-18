
---

```markdown
# Central Difference — Theory

Central difference uses points on both sides of \( x \) to approximate:

\[
f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}
\]

---

## 1. Formula

\[
D_f^{c}(x) = \frac{f(x+h) - f(x-h)}{2h}
\]

---

## 2. Error

For smooth \( f \):

\[
f'(x) = D_f^{c}(x) + O(h^2)
\]

Central difference is **second‑order accurate**, more precise than forward/backward.

---

## 3. Properties

- Higher accuracy for the same \( h \)  
- Requires two function evaluations  
- Symmetric around \( x \)  

---

## 4. Conceptual Example

For:

\[
f(x) = \sin(x),\quad x = 1,\quad h = 10^{-4}
\]

\[
f'(1) \approx \frac{\sin(1+h) - \sin(1-h)}{2h}
\]

which closely matches:

\[
\cos(1) \approx 0.540302
\]

---

# End of Document
```

