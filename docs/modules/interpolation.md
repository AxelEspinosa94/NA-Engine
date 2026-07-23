
---

# 📘 **Interpolation Module — UI & Execution Guide**

## 1. Overview

The **Interpolation Module** of NA‑Engine provides numerical interpolation using four classical methods:

- **Lagrange**
- **Newton**
- **Cubic Splines**
- **Hermite**

The UI supports multiple input modes and dynamically renders results including the interpolating polynomial, node table, plots, and numerical evaluation.

---

## 2. UI Workflow

The complete workflow follows this pattern:

```
Select method → Select input mode → Provide data → Enter xk → Run → View results
```

Each step is described in detail below.

---

## 3. Step 1 — Select Interpolation Method

The user chooses one of the available interpolation methods:

| Method | Description |
|--------|-------------|
| **Lagrange** | Classical interpolating polynomial |
| **Newton** | Divided differences, efficient for incremental nodes |
| **Cubic Splines** | Smooth piecewise interpolation |
| **Hermite** | Interpolation with derivative information |

The selected method determines:

- Required columns (`x, y` or `x, y, dy`)
- Validation rules
- Type of polynomial generated
- Type of plot rendered

---

## 4. Step 2 — Select Input Mode

The module supports **three input modes**, each with its own dynamic UI:

### 4.1 Table Mode
Displays an editable `dash_table.DataTable` with the required columns.

Users can:

- edit cells  
- add rows  
- delete rows  

The callback converts the table into a standardized `DataFrame`.

---

### 4.2 Function Mode
Displays a form to automatically generate nodes:

- `f(x)` — Python-style function (`x**2 + 1`)
- `a, b` — evaluation range
- `n` — number of points

The system:

- evaluates the function at `n` points  
- builds a DataFrame  
- computes `dy = f'(x)` using SymPy when Hermite is selected  

---

### 4.3 Upload Mode
Displays a `dcc.Upload` component with file preview.

Supported formats:

- `.csv`
- `.txt`
- `.xlsx`, `.xls`
- `.json`

The system:

- detects file type  
- parses the content  
- validates required columns  
- converts values to numeric  
- drops invalid rows  

---

## 5. Step 3 — Data Loading

Depending on the selected mode:

| Mode | Data Source |
|------|-------------|
| Table | Editable table |
| Function | Evaluation of f(x) |
| Upload | Uploaded file |

All modes produce a **standardized DataFrame** with the required columns.

---

## 6. Step 4 — Enter xk

The user enters the point at which the interpolating polynomial will be evaluated.

This value is passed directly to the numerical method.

---

## 7. Step 5 — Run Interpolation

When the user clicks **Run**, the callback:

1. Builds the DataFrame according to the selected mode  
2. Validates the input using `InterpolationValidator`  
3. Executes the method using `InterpolationExecutor`  
4. Normalizes the result using `Renderer`  
5. Builds UI blocks using `UIContract`  
6. Renders the final output in `interp-result-area`  

---

## 8. Rendered Results

The dynamic result area displays **independent blocks**, depending on the method and output.

### 8.1 Numerical Result
Markdown with LaTeX:

```
f(x_k) = ⧼value⧽
```

---

### 8.2 Polynomial Expression
Markdown block showing the symbolic polynomial:

```
P(x) = ...
```

---

### 8.3 Node Table
Rendered using `dash_table.DataTable`.

---

### 8.4 Plot
Plotly graph showing:

- interpolating curve  
- original nodes  
- evaluation point xk  

---

### 8.5 Error Blocks
Displayed in red, containing:

- error message  
- error type  
- context  

---

## 9. Internal Architecture

The module uses the full NA‑Engine pipeline:

```
UI → Callbacks → NumericalMethod → Validator → Executor → Renderer → UIContract → Dash Components
```

### Key Components

- `interpolation_callbacks.py` — UI logic  
- `_build_dataframe()` — DataFrame construction  
- `NumericalMethod` — orchestration  
- `InterpolationValidator` — validation  
- `InterpolationExecutor` — numerical computation  
- `Renderer` — payload normalization  
- `UIContract` — block construction  
- `result_view.py` — final rendering  

---

## 10. Example Usage

1. Select **Newton**  
2. Select **Function Mode**  
3. Enter:
   - `f(x) = x**3 - 2*x + 1`
   - `a = 0`
   - `b = 4`
   - `n = 10`
4. Enter `xk = 2.5`  
5. Click **Run**

The system will display:

- interpolated value  
- Newton polynomial  
- node table  
- plot  
- nodes and curve  

---

## 11. Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ValidationError` | insufficient nodes | add more points |
| `FunctionSyntaxError` | invalid function | correct syntax |
| `MissingColumns` | file missing required columns | add columns |
| `ExecutionError` | numerical issues | inspect node distribution |

---

## 12. Extending the Module

To add a new interpolation method:

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

## 13. Optional Screenshots

You may include images showing:

- module UI  
- table  
- plot  
- result blocks  

---
