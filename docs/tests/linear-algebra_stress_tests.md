
---

# **NA‑Engine — Linear Algebra Module Stress Testing Guide**  
### *Continuous Integration / Continuous Deployment (CI/CD) via GitHub Actions*

---

## **Overview**

This document describes the stress‑testing strategy used for the **Linear Algebra Module** of **NA‑Engine**, executed automatically through **GitHub Actions** as part of the CI/CD pipeline.

Stress tests are designed to evaluate:

- Stability under large matrices and high‑dimensional systems  
- Determinism of matrix operations and linear solvers  
- Robustness across all supported linear algebra methods  
- Behavior under malformed or invalid inputs  
- UIContract rendering stability  
- End‑to‑end pipeline consistency (upload → parsing → NumericalMethod → UIContract)

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

Stress tests for linear algebra simulate **real‑world numerical workloads**, not ideal textbook cases.  
The goals are:

1. **Large matrices**  
   Determinants, inverses, and decompositions must remain stable for sizes up to 200×200.

2. **High‑dimensional systems**  
   Solvers (Gauss, QR) must handle systems up to 100 unknowns.

3. **Precision validation**  
   Small matrices are compared against analytical ground truth using NumPy.

4. **Determinism**  
   Repeated runs must produce identical results.

5. **Malformed input handling**  
   Ragged matrices, missing vectors, and invalid shapes must produce controlled errors.

6. **Upload pipeline stability**  
   Text‑based uploads (CSV/TXT/Excel) must parse correctly and feed into NumericalMethod.

7. **UIContract stability**  
   UIContract must always return a valid `html.Div`, even on error.

---

## **Recommended Stress Parameters per Method**

Different linear algebra operations scale differently.  
Using the same matrix size for all methods is **incorrect** and leads to instability or timeouts.

Below are the recommended stress values for each method.

---

### ### **Determinant**

| Property | Recommendation |
|---------|----------------|
| Stress size | **50–200** |
| Reason | Determinant computation is O(n³) but stable for n ≤ 200 |
| Notes | Larger matrices (≥ 300) may cause CI timeouts |

---

### ### **Inverse**

| Property | Recommendation |
|---------|----------------|
| Stress size | **≤ 50** |
| Reason | Matrix inversion is expensive and sensitive to conditioning |
| Notes | Stress tests use small matrices and compare against NumPy |

---

### ### **Rank**

| Property | Recommendation |
|---------|----------------|
| Stress size | **50–200** |
| Reason | Rank computation is stable and fast |
| Notes | Ideal for upload‑based stress tests |

---

### ### **Gauss (Gaussian Elimination)**

| Property | Recommendation |
|---------|----------------|
| Stress size | **≤ 100** |
| Reason | Solving Ax = b is O(n³) and becomes slow for n ≥ 150 |
| Notes | Stress tests validate determinism and solution length |

---

### ### **QR Solver**

| Property | Recommendation |
|---------|----------------|
| Stress size | **≤ 50** |
| Reason | QR decomposition is stable but computationally heavy |
| Notes | Stress tests compare solutions against NumPy ground truth |

---

## **Stress Test Categories**

The stress suite includes the following categories:

---

### **1. Volume Stress — Large Matrices**

Tests with matrices of size 50×50, 100×100, and 200×200 ensure:

- determinant computation does not crash  
- memory usage remains stable  
- execution time stays within CI limits  

---

### **2. Precision Stress — Analytical Ground Truth**

Small matrices are compared against NumPy:

- inverse  
- QR solver  

This ensures:

- numerical consistency  
- correct implementation of decomposition‑based solvers  

---

### **3. Stability Stress — Determinism**

Repeated runs with identical inputs must produce identical outputs.

This validates:

- deterministic solvers  
- stable floating‑point behavior  
- absence of random branching or unstable pivoting  

---

### **4. Error Handling Stress — Invalid Inputs**

Malformed inputs must produce controlled exceptions:

- ragged matrices  
- missing `b` vector for systems  
- invalid shapes  
- non‑square matrices for determinant/inverse  

Stress tests ensure:

- constructor raises `ConstructionError`  
- validator raises `ValidationError`  
- executor raises `ExecutionError` when appropriate  

---

### **5. Upload Stress — TXT / CSV / Excel**

Upload tests simulate Dash’s upload component using Base64‑encoded text.

Stress tests validate:

- correct parsing of matrices  
- correct parsing of linear systems  
- correct integration with NumericalMethod  
- correct rendering via UIContract  

---

### **6. Full Pipeline Stress**

End‑to‑end tests validate:

```
Upload → Parsing → NumericalMethod → Validation → Execution → UIContract → Dash Components
```

These tests ensure:

- payload structure is correct  
- UIContract always returns a valid `html.Div`  
- no part of the pipeline crashes under stress  

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

The stress testing suite ensures that NA‑Engine’s linear algebra module is:

- Stable under large matrices and high‑dimensional systems  
- Robust across all matrix operations and solvers  
- Deterministic and reproducible  
- Safe under malformed inputs  
- UI‑consistent even during errors  
- CI‑friendly and performant  

By using method‑specific stress parameters, NA‑Engine avoids CI timeouts and ensures reliable continuous deployment.

---
