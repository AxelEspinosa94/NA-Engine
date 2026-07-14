
---


# Second Derivative — Theory

Finite differences can approximate the second derivative $f''(x)$.

---

## 1. Forward Second Difference

$$
f''(x) \approx \frac{f(x+2h) - 2f(x+h) + f(x)}{h^2}
$$

---

## 2. Central Second Difference

$$
f''(x) \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}
$$

Central second difference is typically more accurate and symmetric.

---

## 3. Error

For smooth $f$:

$$
f''(x) = D^{(2)}(x) + O(h^2)
$$

---

## 4. Conceptual Example

For:

$$
f(x) = \sin(x)
$$

$$
f''(x) = -\sin(x)
$$

Using central second difference at $x = 1$ approximates:

$$
f''(1) \approx -\sin(1)
$$

---

# End of Document
