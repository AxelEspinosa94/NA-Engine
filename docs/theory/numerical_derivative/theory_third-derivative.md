
---

# Third Derivative — Theory

Higher‑order finite differences can approximate the third derivative $f^{(3)}(x)$.

---

## 1. Forward Third Difference

$$
f^{(3)}(x) \approx \frac{f(x+3h) - 3f(x+2h) + 3f(x+h) - f(x)}{h^3}
$$

This uses four points: $x, x+h, x+2h, x+3h$.

---

## 2. Error

For smooth $f$:

$$
f^{(3)}(x) = D^{(3)}(x) + O(h)
$$

Accuracy depends strongly on $h$ and function smoothness.

---

## 3. Conceptual Example

For:

$$
f(x) = \sin(x)
$$

$$
f^{(3)}(x) = -\cos(x)
$$

Forward third difference at $x = 1$ approximates:

$$
f^{(3)}(1) \approx -\cos(1)
$$

---

# End of Document
