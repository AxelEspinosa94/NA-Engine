
---

# 📘 **Numerical Derivative Module — UI & Execution Guide**

## 1. Overview

The **Numerical Derivative Module** of NA‑Engine provides numerical differentiation using classical finite‑difference formulas, Richardson extrapolation, and partial derivatives for functions of two variables.

Supported methods include:

- **Forward Difference**  
- **Backward Difference**  
- **Central Difference**  
- **Richardson Extrapolation**  
- **Second‑Order Forward**  
- **Second‑Order Central**  
- **Third‑Order Forward**  
- **Partial Derivative ∂/∂x**  
- **Partial Derivative ∂/∂y**

The UI supports function‑based input and dynamically renders results including the numerical derivative, node table, plots, and method‑specific metadata.

This document describes the full UI workflow, execution pipeline, and practical recommendations for each numerical method.

---

## 2. UI Workflow

The complete workflow follows this pattern:

```
Select method → Provide f(x) → Provide x₀ → Provide h → (Optional y₀) → Run → View results
```

Each step is described in detail below.

---

## 3. Step 1 — Select Derivative Method

The user chooses one of the available numerical differentiation methods:

| Method | Description |
|--------|-------------|
| **Forward** | First‑order forward difference |
| **Backward** | First‑order backward difference |
| **Central** | First‑order central difference |
| **Richardson** | Richardson extrapolation using central differences |
| **Second Forward** | Second derivative using forward stencil |
| **Second Central** | Second derivative using central stencil |
| **Third Forward** | Third derivative using forward stencil |
| **Partial ∂/∂x** | Partial derivative w.r.t. x |
| **Partial ∂/∂y** | Partial derivative w.r.t. y |

The selected method determines:

- Required inputs (`x₀`, `h`, and optionally `y₀`)  
- Validation rules  
- Node distribution  
- Type of numerical approximation  
- Whether Richardson order is used  

---

## 4. Step 2 — Provide Function Input

The Derivative Module uses a **single input mode**:

### **Function Mode**

The user provides:

- `f(x)` or `f(x, y)` — Python‑style function (`sin(x) + x**2`, `x*y + y**2`)  
- `x₀` — evaluation point  
- `h` — step size  
- `y₀` — only for partial derivatives  

The system:

1. Normalizes the function (e.g., `sin(x)` → `np.sin(x)`)  
2. Evaluates `f` at the nodes required by the method  
3. Builds a standardized DataFrame  
4. Passes nodes and metadata to the numerical executor  

This mode ensures consistency across all derivative methods.

---

## 5. Step 3 — Data Loading

The module constructs a DataFrame with:

| Column | Meaning |
|--------|---------|
| `x` | Node positions |
| `f(x)` | Function values at nodes |

This DataFrame is used internally by:

- All finite‑difference formulas  
- Richardson extrapolation  
- Plot generation  
- UIContract rendering  

Partial derivatives evaluate `f(x, y)` but still return standardized output.

---

## 6. Step 4 — Run Derivative

When the user clicks **Run**, the callback:

1. Builds the input data from UI fields  
2. Validates the input using `NumericalDerivativeValidator`  
3. Executes the method using `NumericalDerivativeExecutor`  
4. Normalizes the result using `Renderer`  
5. Builds UI blocks using `UIContract`  
6. Renders the final output in `deriv-result-area`  

---

## 7. Rendered Results

The dynamic result area displays **independent blocks**, depending on the method and output.

### 7.1 Numerical Result
Markdown with LaTeX‑style formatting:

```
f'(x₀) ≈ ⧼value⧽
```

or

```
∂f/∂y (x₀, y₀) ≈ ⧼value⧽
```

---

### 7.2 Symbolic‑Style Expression

Generated automatically:

```
f(x) = sin(x) + x²
f'(x₀) ≈ 5.000000
```

or for partials:

```
f(x, y) = x*y + y²
∂f/∂x (x₀, y₀) ≈ 3.000000
```

---

### 7.3 Node Table

Rendered using `dash_table.DataTable`.

Shows:

- nodes used by the finite‑difference stencil  
- function values at each node  

Example:

| x | f(x) |
|---|------|
| x₀ − h | f(x₀ − h) |
| x₀ | f(x₀) |
| x₀ + h | f(x₀ + h) |

---

### 7.4 Plot

Plotly graph showing:

- function curve around `x₀`  
- nodes used by the method  
- step size visualization  

---

### 7.5 Error Blocks

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

- `derivative_callbacks.py` — UI logic  
- `_normalize_function()` — function normalization  
- `NumericalMethod` — orchestration  
- `NumericalDerivativeValidator` — validation  
- `NumericalDerivativeExecutor` — numerical computation  
- `_build_expr()` — symbolic‑style expression generation  
- `Renderer` — payload normalization  
- `UIContract` — block construction  
- `result_view.py` — final rendering  

---

## 9. Practical Recommendations per Method

Different numerical derivative methods behave differently depending on the step size `h`.  
Choosing the same `h` for all methods is **incorrect** and leads to instability or catastrophic cancellation.

Below are recommended values for **production usage**, **UI usage**, and **stress testing**.

---

### **Forward / Backward Difference**

| Property | Recommendation |
|---------|----------------|
| UI h | **1e‑3 to 1e‑2** |
| Stress h | **1e‑6** |
| Notes | First‑order accurate; sensitive to very small h |

---

### **Central Difference**

| Property | Recommendation |
|---------|----------------|
| UI h | **1e‑3** |
| Stress h | **1e‑7** |
| Notes | Second‑order accurate; best general‑purpose method |

---

### **Richardson Extrapolation**

| Property | Recommendation |
|---------|----------------|
| UI order | **2** |
| Stress order | **4–8** |
| Notes | Very accurate but unstable for large h |

---

### **Second‑Order Derivatives**

| Property | Recommendation |
|---------|----------------|
| UI h | **1e‑3** |
| Stress h | **1e‑6** |
| Notes | Sensitive to noise; central stencil preferred |

---

### **Third‑Order Derivatives**

| Property | Recommendation |
|---------|----------------|
| UI h | **1e‑3** |
| Stress h | **1e‑5** |
| Notes | Forward stencil only; unstable for tiny h |

---

### **Partial Derivatives**

| Property | Recommendation |
|---------|----------------|
| UI h | **1e‑3** |
| Stress h | **1e‑6** |
| Notes | Requires `f(x, y)`; uses central difference in the chosen variable |

---

## 10. Example Usage

1. Select **Central**  
2. Enter:
   - `f(x) = sin(x) + x**2`
   - `x₀ = 2.0`
   - `h = 0.01`
3. Click **Run**

The system will display:

- numerical derivative  
- symbolic‑style expression  
- node table  
- function plot  
- metadata  

---

## 11. Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ConstructionError` | invalid variable in function | ensure only x or x,y appear |
| `ValidationError` | missing y in partial derivative | provide y₀ |
| `ExecutionError` | function evaluation failure | check syntax or domain |
| `ZeroDivisionError` | h = 0 | choose positive h |
| `CatastrophicCancellation` | h too small | increase h |

---

## 12. Extending the Module

To add a new derivative method:

1. Add entry in `method_catalog.json`  
2. Implement constructor logic if new variables are needed  
3. Implement validator rules  
4. Implement executor formula  
5. Add UI option  
6. Add callback logic if special inputs are required  

No changes are needed in:

- `NumericalMethod`  
- `Renderer`  
- `UIContract`  
- `result_view`  

---
