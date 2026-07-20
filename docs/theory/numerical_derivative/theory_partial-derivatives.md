
---

# Partial Derivatives — Theory

For a function of two variables:

$$
f(x, y)
$$

the partial derivatives measure change with respect to one variable while holding the other constant.

---

## 1. Partial w.r.t. x

$$
\frac{\partial f}{\partial x}(x,y)
\approx \frac{f(x+h,y) - f(x-h,y)}{2h}
$$

This is a central difference in the $x$ direction.

---

## 2. Partial w.r.t. y

$$
\frac{\partial f}{\partial y}(x,y)
\approx \frac{f(x,y+h) - f(x,y-h)}{2h}
$$

Central difference in the $y$ direction.

---

## 3. Properties

- Requires function evaluation in a grid around \((x,y)\)  
- Accuracy depends on $h$ and smoothness of $f$  
- Extends naturally to higher dimensions  

---

## 4. Conceptual Example

For:

$$
f(x,y) = x^2 + y^2
$$

Exact partials:

$$
\frac{\partial f}{\partial x} = 2x,\quad
\frac{\partial f}{\partial y} = 2y
$$

Finite differences at \((1,1)\) approximate:

$$
\frac{\partial f}{\partial x}(1,1) \approx 2,\quad
\frac{\partial f}{\partial y}(1,1) \approx 2
$$

---

# End of Document
```

---

