
---

# Trapezoidal Rule — Theory

The trapezoidal rule is one of the simplest numerical integration techniques.  
It approximates the area under a curve by dividing the interval into trapezoids.

---

# 1. Simple Trapezoid Rule

Given a function $f(x)$ on the interval $[a, b]$, the simple trapezoid rule uses:

$$
T = \frac{b - a}{2} \left[f(a) + f(b)\right]
$$

This corresponds to approximating the curve with a single trapezoid.

---

# 2. Composite Trapezoid Rule

For $n$ subintervals of equal width:

$$
h = \frac{b - a}{n}
$$

The composite rule is:

$$
T = h\left[\frac{f(x_0)}{2} + \sum_{i=1}^{n-1} f(x_i) + \frac{f(x_n)}{2}\right]
$$

where:

$$
x_i = a + ih
$$

---

# 3. Properties

### Advantages
- Very simple
- Works for any continuous function
- Good for coarse approximations

### Disadvantages
- Low accuracy (order $O(h^2)$)
- Requires many subintervals for good precision

---

# 4. Conceptual Example

For:

$$
f(x) = x^2,\quad [0, 2]
$$

Simple trapezoid:

$$
T = \frac{2}{2}(0^2 + 2^2) = 4
$$

Exact integral:

$$
\int_0^2 x^2 dx = \frac{8}{3} \approx 2.6667
$$

The trapezoid rule overestimates the area.

---

# End of Document

