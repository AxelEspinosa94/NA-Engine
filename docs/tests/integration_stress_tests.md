
---

# **NA‑Engine — Integration Module Stress Testing Guide**
### *Continuous Integration / Continuous Deployment (CI/CD) via GitHub Actions*

---

## **Overview**

This document describes the stress‑testing strategy used for the **Numerical Integration Module** of **NA‑Engine**, executed automatically through **GitHub Actions** as part of the CI/CD pipeline.

Stress tests are designed to evaluate:

- Stability under large workloads  
- Determinism of numerical results  
- Robustness across all supported integration methods  
- Behavior under difficult or pathological inputs  
- UIContract rendering stability  

These tests **do not evaluate accuracy**, which is already covered by unit tests.  
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

Stress tests in NA‑Engine aim to simulate **heavy real‑world usage**, not mathematical precision.  
The goals are:

1. **Large n values**  
   Ensure the executor handles large partitions without crashing.

2. **All integration methods**  
   Every method is tested under stress, including:
   - Trapezoid (simple & composite)
   - Simpson (1/3 and 3/8)
   - Romberg
   - Gauss‑Legendre

3. **Difficult functions**  
   Functions without elementary primitives (e.g., `exp(-x**2)`, `sin(x)/x`)  
   and functions with singularities (e.g., `1/x`) are included.

4. **Determinism**  
   The same input must always produce the same output.

5. **UI stability**  
   UIContract must always return a valid `html.Div`, even on error.

---

## **Recommended Stress Parameters per Method**

Different numerical methods scale differently.  
Using the same `n` for all methods is **incorrect** and leads to instability or timeouts.

Below are the recommended stress values for each method.

---

### ### **Trapezoid (Simple)**

| Property | Recommendation |
|---------|----------------|
| Stress n | **1** |
| Reason | Method is defined only for one interval |
| Notes | Precision is low by design; stress tests only check stability |

---

### ### **Trapezoid (Composite)**

| Property | Recommendation |
|---------|----------------|
| Stress n | **≈ 300** |
| Reason | Linear complexity, stable for large n |
| Notes | Good baseline method for stress testing |

---

### ### **Simpson 1/3**

| Property | Recommendation |
|---------|----------------|
| Stress n | **≈ 300** |
| Reason | Requires even number of subintervals; stable for large n |
| Notes | Good balance between speed and stability |

---

### ### **Simpson 3/8**

| Property | Recommendation |
|---------|----------------|
| Stress n | **≈ 300**, must be **multiple of 3** |
| Reason | Method requires n % 3 == 0 |
| Notes | Very stable when n is valid; unstable otherwise |

---

### ### **Romberg**

| Property | Recommendation |
|---------|----------------|
| Stress n | **6** |
| Reason | Romberg is O(n²) in time and memory |
| Notes | n > 6 causes CI timeouts; n = 6 is the practical sweet spot |

#### **Practical Romberg Guidance**

Romberg builds a triangular extrapolation table of size `(n+1) × (n+1)`.

- n = 6 → 49 cells → fast and stable  
- n = 10 → 121 cells → slow  
- n = 20 → 441 cells → very slow  
- n = 50 → 2601 cells → CI timeout  
- n = 100 → 10,201 cells → impractical  

Even on an 8 GB RAM machine, Romberg becomes **CPU‑bound**, not memory‑bound.

**Recommendation:**  
Use **n ∈ [4, 6]** for all stress tests and production usage.

---

### ### **Gauss‑Legendre**

| Property | Recommendation |
|---------|----------------|
| Stress n | **10–15 points** |
| Reason | Gauss is extremely stable and fast |
| Notes | More points increase accuracy but not stress value |

#### **Practical Gauss‑Legendre Guidance**

- Gauss‑Legendre is exact for polynomials up to degree `2n − 1`.  
- Increasing points increases accuracy, not stress.  
- Very high n (≥ 50) is unnecessary and slows down CI.

**Recommendation:**  
Use **10–15 points** for stress tests.

---

## **Stress Test Categories**

The stress suite includes the following categories:

### **1. Volume Stress**
Large n values to ensure stability.

### **2. Determinism**
Repeated runs must produce identical results.

### **3. Interval Stress**
Negative intervals and unit intervals.

### **4. Non‑elementary Functions**
Functions without closed‑form primitives.

### **5. Singularities**
Functions like `1/x` must produce controlled errors.

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

The stress testing suite ensures that NA‑Engine’s integration module is:

- Stable under heavy workloads  
- Robust across all numerical methods  
- Deterministic and reproducible  
- Safe under pathological inputs  
- UI‑consistent even during errors  
- CI‑friendly and performant  

By using method‑specific stress parameters, NA‑Engine avoids CI timeouts and ensures reliable continuous deployment.

---
