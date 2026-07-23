
---

# **NA‑Engine — ODE Module Stress Testing Guide**  
### *Continuous Integration / Continuous Deployment (CI/CD) via GitHub Actions*

---

## **Overview**

This document describes the stress‑testing strategy used for the **Ordinary Differential Equations (ODE) Module** of **NA‑Engine**, executed automatically through **GitHub Actions** as part of the CI/CD pipeline.

Stress tests are designed to evaluate:

- Stability under extreme values of `x`, `y`, and step size `h`  
- Robustness of IVP solvers (Euler, Heun, RK2, RK4, Adams family)  
- Stability of system solvers (RK4 System)  
- Behavior of BVP solvers (Shooting, Finite Differences) under difficult boundary conditions  
- Determinism across all ODE modes  
- UIContract rendering stability  
- End‑to‑end pipeline consistency  

These tests **do not evaluate mathematical accuracy**, which is already covered by unit tests.  
Instead, they focus on **performance, resilience, and reliability** under stress.

---

## **CI/CD Strategy**

NA‑Engine uses **GitHub Actions** to automatically run stress tests on every push or pull request.

Only tests marked with:

```python
@pytest.mark.pending
```

are executed in CI.

Once a module is stable, the `pending` marker is removed, and the test is excluded from CI runs.

This approach ensures:

- Fast CI cycles  
- Controlled rollout of stress tests  
- Ability to gradually harden modules  
- Avoidance of unnecessary load on GitHub runners  

---

## **Stress Testing Philosophy**

Stress tests for ODEs simulate **real‑world numerical challenges**, not ideal textbook cases.  
The goals are:

1. **Extreme values of x and y**  
   Ensure solvers remain stable under large domains.

2. **Extreme values of h**  
   Test precision limits (very small h) and instability (very large h).

3. **All ODE modes**  
   Every method is tested under stress, including:
   - Euler  
   - Heun  
   - RK2  
   - RK4  
   - RK4 System  
   - Shooting  
   - Finite Differences  
   - Adams–Bashforth 2  
   - Adams–Bashforth 3  
   - Adams–Moulton 2  

4. **Oscillatory functions**  
   Functions like `sin(100x)` test numerical sensitivity.

5. **Large systems**  
   RK4 System must handle vector ODEs with many components.

6. **Boundary Value Problems**  
   Shooting and Finite Differences must remain stable under difficult boundary conditions.

7. **Determinism**  
   The same input must always produce the same output.

8. **UI stability**  
   UIContract must always return a valid `html.Div`, even on error.

---

## **Recommended Stress Parameters per Method**

Different ODE solvers behave differently under stress.  
Using the same `h` for all methods is **incorrect** and leads to instability or misleading results.

Below are the recommended stress values for each method.

---

### **Euler / Heun / RK2 / RK4**

| Property | Recommendation |
|---------|----------------|
| Stress x | **0 → 500** |
| Stress h (small) | **1e‑6** |
| Stress h (large) | **5.0** |
| Notes | Euler is least stable; RK4 is most stable |

---

### **Adams–Bashforth / Adams–Moulton**

| Property | Recommendation |
|---------|----------------|
| Stress h | **1e‑3 → 1.0** |
| Notes | Multistep methods amplify instability |

---

### **RK4 System**

| Property | Recommendation |
|---------|----------------|
| Dimension | **5 → 10 equations** |
| Stress h | **0.01 → 0.1** |
| Notes | Sensitive to stiffness and coupling |

---

### **Shooting Method**

| Property | Recommendation |
|---------|----------------|
| Interval | **0 → 10** |
| Initial slope | **random in [-5, 5]** |
| Notes | Highly sensitive to slope guess |

---

### **Finite Differences**

| Property | Recommendation |
|---------|----------------|
| n | **100 → 300** |
| Notes | Large matrices test conditioning and solver stability |

---

## **Stress Test Categories**

The stress suite includes the following categories:

---

### **1. Large Intervals**

Tests with `x_end = 500` ensure:

- IVP solvers do not overflow  
- RK4 remains stable  
- UIContract can render large arrays  

---

### **2. Very Small h (Precision Stress)**

Tests with `h = 1e‑6` validate:

- floating‑point stability  
- correct handling of near‑zero increments  
- absence of NaN or infinity  

---

### **3. Very Large h (Instability Stress)**

Tests with `h = 5.0` ensure:

- solvers remain stable under coarse approximations  
- no crashes due to domain issues  

---

### **4. Highly Oscillatory Functions**

Functions like `sin(100x)` test:

- sensitivity to step size  
- stability of RK methods  
- correct parsing of trigonometric expressions  

---

### **5. Large Systems (RK4 System)**

Systems with 10 equations validate:

- vectorized RK4 stability  
- correct handling of multiple dependent variables  
- UIContract multi‑curve rendering  

---

### **6. Shooting Method Stress**

Difficult BVPs test:

- slope sensitivity  
- IVP solver stability inside shooting  
- correct boundary matching  

---

### **7. Finite Differences with Large n**

Large grids validate:

- matrix conditioning  
- solver stability  
- correct boundary incorporation  

---

### **8. Determinism**

Repeated runs validate:

- reproducibility  
- absence of randomness  
- consistent floating‑point behavior  

---

## **Why Accuracy Is Not Tested Here**

Accuracy is fully covered by:

- Unit tests  
- Method‑specific tests  
- Mathematical validation tests  

Stress tests focus exclusively on:

- Stability  
- Performance  
- Determinism  
- Robustness  
- UI rendering  

This separation keeps CI fast and avoids unnecessary computational load.

---

## **Conclusion**

The stress testing suite ensures that NA‑Engine’s ODE module is:

- Stable under extreme values of x, y, and h  
- Robust across IVP, system, and BVP solvers  
- Deterministic and reproducible  
- Safe under oscillatory and stiff‑like inputs  
- UI‑consistent even during errors  
- CI‑friendly and performant  

By using method‑specific stress parameters, NA‑Engine avoids CI timeouts and ensures reliable continuous deployment.

---

