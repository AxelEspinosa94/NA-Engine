
---


```markdown
# RK4 for Systems of ODEs — Theory

For a system:

$$
\mathbf{y}' = \mathbf{f}(x, \mathbf{y}), \quad \mathbf{y}(x_0) = \mathbf{y}_0
$$

RK4 generalizes by treating $\mathbf{y}$ as a vector.

---

## 1. Vector Form

$$
\mathbf{y}_{n+1} = \mathbf{y}_n + \frac{h}{6}
(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)
$$

where:

$$
\begin{aligned}
\mathbf{k}_1 &= \mathbf{f}(x_n, \mathbf{y}_n) \\
\mathbf{k}_2 &= \mathbf{f}\left(x_n + \frac{h}{2}, \mathbf{y}_n + \frac{h}{2}\mathbf{k}_1\right) \\
\mathbf{k}_3 &= \mathbf{f}\left(x_n + \frac{h}{2}, \mathbf{y}_n + \frac{h}{2}\mathbf{k}_2\right) \\
\mathbf{k}_4 &= \mathbf{f}(x_n + h, \mathbf{y}_n + h\mathbf{k}_3)
\end{aligned}
$$

---

## 2. Properties

- Same order: $O(h^4)$  
- Works component‑wise on each equation  
- Natural for systems like mechanics, circuits, etc.

---

## 3. Conceptual Example

System:

$$
\begin{cases}
y_1' = y_2 \\
y_2' = -y_1
\end{cases}
$$

describes harmonic motion; RK4 approximates sine and cosine.

---

# End of Document
```

