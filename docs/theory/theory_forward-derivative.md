
---

# Forward Difference — Theory

Forward difference approximates the first derivative of a function:

\[
f'(x) \approx \frac{f(x+h) - f(x)}{h}
\]

where \( h > 0 \) is a small step size.

---

## 1. Formula

\[
D_f^{+}(x) = \frac{f(x+h) - f(x)}{h}
\]

This uses the point \( x \) and a forward point \( x+h \).

---

## 2. Error

For smooth \( f \):

\[
f'(x) = D_f^{+}(x) - \frac{h}{2}f''(x) + O(h^2)
\]

So the method is **first‑order accurate** in \( h \).

---

## 3. Properties

- Simple and easy to implement  
- Requires only one extra function evaluation  
- Less accurate than central difference  

---

## 4. Conceptual Example

For:

\[
f(x) = \sin(x),\quad x = 1,\quad h = 10^{-4}
\]

\[
f'(1) \approx \frac{\sin(1 + h) - \sin(1)}{h}
\]

which approximates:

\[
\cos(1) \approx 0.540302
\]

---

# End of Document


