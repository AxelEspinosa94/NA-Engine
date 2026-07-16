
---

# **NA‑Engine — Numerical Derivatives Module Stress Testing Guide**  
### *Continuous Integration / Continuous Deployment (CI/CD) via GitHub Actions*

---

## **Overview**

This document describes the stress‑testing strategy used for the **Numerical Derivatives Module** of **NA‑Engine**, executed automatically through **GitHub Actions** as part of the CI/CD pipeline.

Stress tests are designed to evaluate:

- Stability under extreme values of `x` and `h`  
- Determinism across all derivative modes  
- Robustness under oscillatory or pathological functions  
- Behavior under mixed‑variable partial derivatives  
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

Stress tests for numerical derivatives simulate **real‑world numerical challenges**, not ideal textbook cases.  
The goals are:

1. **Extreme values of x**  
   Ensure derivative formulas remain stable for very large inputs.

2. **Extreme values of h**  
   Test precision limits (very small h) and instability (very large h).

3. **All derivative modes**  
   Every method is tested under stress, including:
   - Forward  
   - Backward  
   - Central  
   - Richardson  
   - Second‑order forward  
   - Second‑order central  
   - Third‑order forward  
   - Partial derivatives (x and y)

4. **Oscillatory functions**  
   Functions like `sin(100x)` test numerical sensitivity.

5. **Mixed‑variable partial derivatives**  
   Ensure correct handling of multi‑variable expressions.

6. **Determinism**  
   The same input must always produce the same output.

7. **UI stability**  
   UIContract must always return a valid `html.Div`, even on error.

---

## **Recommended Stress Parameters per Method**

Different derivative formulas behave differently under stress.  
Using the same `h` for all methods is **incorrect** and leads to instability or misleading results.

Below are the recommended stress values for each method.

---

### ### **Forward / Backward / Central**

| Property | Recommendation |
|---------|----------------|
| Stress x | **1e6** |
| Stress h | **1e‑10 to 1e‑3** |
| Notes | Very small h may amplify floating‑point noise |

---

### ### **Richardson Extrapolation**

| Property | Recommendation |
|---------|----------------|
| Stress order | **2, 4, 6, 8** |
| Stress h | **1e‑3** |
| Notes | Higher orders increase numerical sensitivity |

---

### ### **Second‑Order Forward / Central**

| Property | Recommendation |
|---------|----------------|
| Stress h | **1e‑10 to 1e‑3** |
| Notes | Second‑order formulas are more stable than first‑order |

---

### ### **Third‑Order Forward**

| Property | Recommendation |
|---------|----------------|
| Stress h | **1e‑3** |
| Notes | Third‑order formulas amplify oscillatory behavior |

---

### ### **Partial Derivatives (x and y)**

| Property | Recommendation |
|---------|----------------|
| Stress x, y | **random values in [-50, 50]** |
| Stress h | **1e‑2** |
| Notes | Mixed‑variable expressions must be parsed correctly |

---

## **Stress Test Categories**

The stress suite includes the following categories:

---

### **1. Large x Values**

Tests with `x = 1e6` ensure:

- derivative formulas do not overflow  
- lambdified functions remain stable  
- UIContract can render large numerical outputs  

---

### **2. Very Small h (Precision Stress)**

Tests with `h = 1e‑10` validate:

- floating‑point stability  
- correct handling of near‑zero increments  
- absence of NaN or infinity in derivative formulas  

---

### **3. Very Large h (Instability Stress)**

Tests with `h = 50` ensure:

- formulas remain stable under coarse approximations  
- UIContract still returns valid payloads  
- no crashes due to domain issues (e.g., log(x))  

---

### **4. Highly Oscillatory Functions**

Functions like `sin(100x)` test:

- sensitivity to step size  
- stability of forward/backward/central formulas  
- correct parsing of trigonometric expressions  

---

### **5. Partial Derivatives with Mixed Variables**

Expressions like:

```
x*y + sin(x*y) + y**3
```

validate:

- correct multi‑variable parsing  
- correct substitution of x and y  
- stability under mixed‑variable differentiation  

---

### **6. Richardson with High Order**

Orders 2, 4, 6, 8 test:

- stability of recursive Richardson formulas  
- correct handling of repeated evaluations  
- absence of floating‑point blow‑ups  

---

### **7. Randomized Inputs (Monte Carlo Stress)**

Random tests validate:

- determinism  
- robustness under unpredictable inputs  
- correct handling of extreme values  
- UIContract stability  

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

The stress testing suite ensures that NA‑Engine’s numerical derivatives module is:

- Stable under extreme values of x and h  
- Robust across all derivative formulas  
- Deterministic and reproducible  
- Safe under oscillatory and mixed‑variable inputs  
- UI‑consistent even during errors  
- CI‑friendly and performant  

By using method‑specific stress parameters, NA‑Engine avoids CI timeouts and ensures reliable continuous deployment.

---
