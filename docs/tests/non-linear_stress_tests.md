
---

# **NA‑Engine — Nonlinear Equations Module Stress Testing Guide**  
### *Continuous Integration / Continuous Deployment (CI/CD) via GitHub Actions*

---

## **Overview**

This document describes the stress‑testing strategy used for the **Nonlinear Equations Module** of **NA‑Engine**, executed automatically through **GitHub Actions** as part of the CI/CD pipeline.

Stress tests are designed to evaluate:

- Stability under difficult or pathological numerical conditions  
- Determinism of iterative root‑finding methods  
- Robustness across all supported nonlinear solvers  
- Behavior under divergence scenarios  
- UIContract rendering stability  

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

Stress tests for nonlinear solvers simulate **real‑world numerical challenges**, not ideal textbook cases.  
The goals are:

1. **Difficult functions**  
   Highly oscillatory, discontinuous, or stiff functions.

2. **All nonlinear methods**  
   Every solver is tested under stress, including:
   - Bisection  
   - False Position  
   - Newton  
   - Secant  
   - Fixed Point  

3. **Divergence scenarios**  
   Inputs intentionally designed to break convergence.

4. **Determinism**  
   The same input must always produce the same output.

5. **UI stability**  
   UIContract must always return a valid `html.Div`, even on error.

6. **Payload consistency**  
   Error payloads must follow NA‑Engine’s architecture.

---

## **Recommended Stress Parameters per Method**

Different nonlinear methods behave very differently under stress.  
Using the same parameters for all methods is **incorrect** and leads to instability or misleading results.

Below are the recommended stress values for each method.

---

### ### **Bisection**

| Property | Recommendation |
|---------|----------------|
| Interval | Must satisfy `f(a) * f(b) < 0` |
| Stress interval | Large intervals (e.g., `[-1e6, 1e6]`) |
| Notes | Extremely robust; ideal for stress testing |

---

### ### **False Position**

| Property | Recommendation |
|---------|----------------|
| Interval | Must satisfy `f(a) * f(b) < 0` |
| Stress interval | Large intervals |
| Notes | Faster than bisection but less stable under pathological functions |

---

### ### **Newton**

| Property | Recommendation |
|---------|----------------|
| Stress x0 | Values near derivative zero |
| Notes | Very fast but sensitive to derivative issues; ideal for divergence tests |

#### **Practical Newton Guidance**

Newton fails when:

- `f'(x0) = 0`  
- `f'(x0)` is extremely small  
- `f(x0)` is undefined  
- the next iteration produces NaN or infinity  

Stress tests intentionally include such cases.

---

### ### **Secant**

| Property | Recommendation |
|---------|----------------|
| Stress x0, x1 | Nearly identical values (small denominator) |
| Notes | Must handle near‑zero denominators gracefully |

#### **Practical Secant Guidance**

The denominator:

\[
f(x_1) - f(x_0)
\]

may be extremely small but still valid.  
Stress tests ensure the method:

- does not crash  
- returns a valid payload  
- converges or diverges deterministically  

---

### ### **Fixed Point**

| Property | Recommendation |
|---------|----------------|
| Stress g(x) | Functions where `|g'(x)| ≥ 1` |
| Notes | Ideal for divergence and stability tests |

#### **Practical Fixed Point Guidance**

Fixed Point iteration fails when:

- `|g'(x0)| ≥ 1`  
- g(x) produces NaN or infinity  
- g(x) pushes the iteration outside the domain  

Stress tests intentionally include such cases.

---

## **Stress Test Categories**

The stress suite includes the following categories:

### **1. Divergence Stress**
Inputs designed to break convergence (Newton, Fixed Point).

### **2. Interval Stress**
Large intervals for bisection and false position.

### **3. Oscillatory Functions**
Functions like `sin(50*x)` to test stability.

### **4. Near‑Zero Denominator**
Secant method stability under small denominators.

### **5. Determinism**
Repeated runs must produce identical results.

### **6. Result Structure**
All required keys must be present in the result payload.

### **7. UIContract Stability**
UIContract must always return a valid `html.Div`.

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

The stress testing suite ensures that NA‑Engine’s nonlinear equations module is:

- Stable under difficult numerical conditions  
- Robust across all nonlinear solvers  
- Deterministic and reproducible  
- Safe under divergence scenarios  
- UI‑consistent even during errors  
- CI‑friendly and performant  

By using method‑specific stress parameters, NA‑Engine avoids CI timeouts and ensures reliable continuous deployment.

---
