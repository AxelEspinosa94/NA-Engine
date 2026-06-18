
---


```markdown
# Euler Method — Theory

Euler’s method is the simplest numerical scheme for solving the initial value problem:

\[
y' = f(x, y), \quad y(x_0) = y_0
\]

---

## 1. Idea

From the differential equation:

\[
y' = \frac{dy}{dx} \approx \frac{y_{n+1} - y_n}{h}
\]

we obtain:

\[
y_{n+1} = y_n + h f(x_n, y_n)
\]

---

## 2. Algorithm

Given step size \( h \) and grid:

\[
x_n = x_0 + n h
\]

iterate:

\[
y_{n+1} = y_n + h f(x_n, y_n)
\]

---

## 3. Error and Properties

- Local truncation error: \( O(h^2) \)  
- Global error: \( O(h) \) (first‑order method)  
- Simple but not very accurate  
- Can be unstable for stiff problems

---

## 4. Conceptual Example

\[
y' = y,\quad y(0) = 1
\]

Euler:

\[
y_{n+1} = y_n + h y_n = (1 + h) y_n
\]

Exact solution: \( y(x) = e^x \).

---

# End of Document
```

