
---

# 📘 **Integration Module — UI & Execution Guide**

## 1. Overview

The **Integration Module** of NA‑Engine provides numerical integration using six classical methods:

- **Trapezoid (Simple)**
- **Trapezoid (Composite)**
- **Simpson 1/3**
- **Simpson 3/8**
- **Romberg**
- **Gauss‑Legendre**
- **Clenshaw-Curtis**

The UI supports function‑based input and dynamically renders results including the numerical approximation, node table, plots, and method‑specific metadata.

This document describes the full UI workflow, execution pipeline, and practical recommendations for each numerical method.

---

## 2. UI Workflow

The complete workflow follows this pattern:

```
Select method → Provide f(x) → Provide interval [a, b] → Provide n → Run → View results
```

Each step is described in detail below.

---

## 3. Step 1 — Select Integration Method

The user chooses one of the available numerical integration methods:

| Method | Description |
|--------|-------------|
| **Trapezoid (Simple)** | Single‑interval trapezoid rule |
| **Trapezoid (Composite)** | Multi‑interval trapezoid rule |
| **Simpson 1/3** | Quadratic interpolation on pairs of intervals |
| **Simpson 3/8** | Cubic interpolation on triplets of intervals |
| **Romberg** | Richardson extrapolation over trapezoid refinements |
| **Gauss‑Legendre** | Gaussian quadrature with Legendre nodes |
| **Clenshaw-Curtis** | Quadrature based on Chebyshev nodes |

The selected method determines:

- Required number of subintervals  
- Validation rules  
- Node distribution  
- Type of numerical approximation  
- Additional parameters (e.g., Gauss points)

---

## 4. Step 2 — Provide Function Input

The Integration Module uses a **single input mode**:

### **Function Mode**

The user provides:

- `f(x)` — Python‑style function (`sin(x) + x**2`)
- `a, b` — integration interval
- `n` — number of subintervals or refinement level

The system:

1. Evaluates `f(x)` at `n + 1` nodes  
2. Builds a standardized DataFrame  
3. Passes nodes and metadata to the numerical executor  

This mode ensures consistency across all integration methods.

---

## 5. Step 3 — Data Loading

The module constructs a DataFrame with:

| Column | Meaning |
|--------|---------|
| `x` | Node positions |
| `y` | Function values |

This DataFrame is used internally by:

- Composite rules  
- Simpson rules  
- Plot generation  
- UIContract rendering  

Romberg and Gauss‑Legendre compute their own nodes but still return standardized output.

---

## 6. Step 4 — Run Integration

When the user clicks **Run**, the callback:

1. Builds the DataFrame from `f(x)`  
2. Validates the input using `IntegrationValidator`  
3. Executes the method using `IntegrationExecutor`  
4. Normalizes the result using `Renderer`  
5. Builds UI blocks using `UIContract`  
6. Renders the final output in `integr-result-area`  

---

## 7. Rendered Results

The dynamic result area displays **independent blocks**, depending on the method and output.

### 7.1 Numerical Result
Markdown with LaTeX:

```
∫_a^b f(x) dx ≈ ⧼value⧽
```

---

### 7.2 Node Table
Rendered using `dash_table.DataTable`.

Shows:

- nodes used for composite rules  
- evaluation points for Gauss‑Legendre  
- refinement levels for Romberg  

---

### 7.3 Plot
Plotly graph showing:

- function curve  
- integration interval  
- nodes used by the method  

---

### 7.4 Error Blocks
Displayed in red, containing:

- error message  
- error type  
- context  

---

## 8. Internal Architecture

The module uses the full NA‑Engine pipeline:

```
UI → Callbacks → NumericalMethod → Validator → Executor → Renderer → UIContract → Dash Components
```

### Key Components

- `integration_callbacks.py` — UI logic  
- `_build_function_dataframe()` — DataFrame construction  
- `NumericalMethod` — orchestration  
- `IntegrationValidator` — validation  
- `IntegrationExecutor` — numerical computation  
- `Renderer` — payload normalization  
- `UIContract` — block construction  
- `result_view.py` — final rendering  

---

## 9. Practical Recommendations per Method

Different numerical methods scale differently.  
Using the same `n` for all methods is **incorrect** and leads to instability or timeouts.

Below are the recommended values for **production usage**, **UI usage**, and **stress testing**.

---

### ### **Trapezoid (Simple)**

| Property | Recommendation |
|---------|----------------|
| Valid n | **1** |
| Notes | Defined only for one interval; not intended for high precision |

---

### ### **Trapezoid (Composite)**

| Property | Recommendation |
|---------|----------------|
| UI n | **50–200** |
| Stress n | **≈ 300** |
| Notes | Linear complexity; stable for large n |

---

### ### **Simpson 1/3**

| Property | Recommendation |
|---------|----------------|
| UI n | **50–200** |
| Stress n | **≈ 300** |
| Notes | Requires even number of subintervals; stable for large n |

---

### ### **Simpson 3/8**

| Property | Recommendation |
|---------|----------------|
| UI n | **60–180**, must be **multiple of 3** |
| Stress n | **≈ 300**, must be **multiple of 3** |
| Notes | Unstable if n % 3 ≠ 0 |

---

### ### **Romberg**

| Property | Recommendation |
|---------|----------------|
| UI n | **4–6** |
| Stress n | **6** |
| Notes | O(n²) complexity; n > 6 causes CI timeouts |

#### **Romberg Practical Guidance**

Romberg builds a triangular extrapolation table:

- n = 6 → fast and stable  
- n = 10 → slow  
- n = 20 → very slow  
- n = 50 → CI timeout  
- n = 100 → impractical  

Even on an 8 GB RAM machine, Romberg becomes **CPU‑bound**, not memory‑bound.

---

### ### **Gauss‑Legendre**

| Property | Recommendation |
|---------|----------------|
| UI points | **6–10** |
| Stress points | **10–15** |
| Notes | Extremely stable; more points increase accuracy, not stress |

#### **Gauss‑Legendre Practical Guidance**

- Exact for polynomials up to degree `2n − 1`  
- Very high n (≥ 50) is unnecessary  
- Increasing points increases accuracy, not stress  

---

### ### **Clenshaw–Curtis**

| Property | Recommendation |
|---------|----------------|
| UI points | **8–20** |
| Stress points | **20–40** |
| Notes | Spectral accuracy; extremely stable; even‑N required |

---

#### **Clenshaw–Curtis Practical Guidance**

- Accuracy improves **spectrally** (almost exponentially) as N increases  
- Works best when the integrand is **smooth** on $[a,b]$
- Requires **even N** because the integral uses only cosine modes $a_{2k}$
- Increasing N increases accuracy, not stress — similar to Gauss  
- For highly oscillatory functions, CC often outperforms Gauss with fewer points  
- For smooth functions (polynomials, exponentials, trig), CC converges extremely fast  
- Very high $N$ ($\geq 50$) is rarely needed; diminishing returns after $\approx 40$  
- Clenshaw-Curtis is ideal for UI because the DCT‑I is stable and predictable  
- Clenshaw-CurtisC is ideal for stress tests because the cost grows linearly and the transform is efficient  

---

#### **Recommended Usage**

#### **UI / Normal Use**
- **8–20 points**  
  Perfect balance between speed and accuracy.  
  Most smooth functions converge to machine precision in this range.

#### **Stress Testing**
- **20–40 points**  
  Pushes the DCT‑I and cosine expansion harder.  
  Still extremely stable — CC does not “blow up” like high‑order Newton–Cotes.

#### **Avoid**
- Odd N (breaks the cosine‑mode formula)  
- N > 50 (no practical gain; slower without improving accuracy)  
- Using CC for discontinuous functions (spectral ringing / Gibbs phenomenon)

---

#### **Why These Recommendations Work**

Clenshaw–Curtis is a **spectral method**, meaning:

$$
\text{Error} \sim O\left(\frac{1}{N^p}\right) \quad \text{or even faster}
$$

for smooth functions.

This is why:

- Clenshaw-Curtis with **10 points** often matches Gauss with **20 points**  
- Clenshaw-Curtis with **20 points** often matches composite Simpson with **200+ points**  
- Clenshaw-Curtis with **40 points** is already near machine precision for most analytic functions  

---

### **Short Summary**

- Exact for all cosine expansions up to mode $2N$  
- Very high N (≥ 50) is unnecessary  
- Increasing points increases accuracy, not stress  
- Requires even N  
- Spectral convergence for smooth functions  


---

## 10. Example Usage

1. Select **Simpson 1/3**  
2. Enter:
   - `f(x) = sin(x) + x**2`
   - `a = 0`
   - `b = 4`
   - `n = 120`
3. Click **Run**

The system will display:

- numerical approximation  
- node table  
- function plot  
- interval metadata  

---

## 11. Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ValidationError` | invalid n for method | adjust n (e.g., multiple of 3 for Simpson 3/8) |
| `FunctionSyntaxError` | invalid function | correct syntax |
| `ExecutionError` | numerical instability | reduce n or adjust interval |
| `ZeroDivisionError` | singularity in function | adjust interval |

---

## 12. Extending the Module

To add a new integration method:

1. Add entry in `method_catalog.json`  
2. Implement constructor  
3. Implement validator  
4. Implement executor  
5. Add UI option  
6. Add callback logic if special inputs are required  

No changes are needed in:

- `NumericalMethod`  
- `Renderer`  
- `UIContract`  
- `result_view`  

---

