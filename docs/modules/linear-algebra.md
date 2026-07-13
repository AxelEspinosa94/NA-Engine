
---

# 📘 **Linear Algebra Module — UI & Execution Guide**

## 1. Overview

The **Linear Algebra Module** of NA‑Engine provides matrix operations and linear system solvers through a unified UI and execution pipeline. It supports:

### **Matrix Operations**
- Determinant  
- Inverse  
- Norm  
- Condition Number  
- Transpose  
- Rank  

### **Linear System Solvers**
- Gauss  
- Gauss‑Jordan  
- LU  
- Cholesky  
- QR  
- Jacobi  
- Gauss‑Seidel  

The module accepts input either through **manual table entry** or **file upload**, and renders results using standardized UI blocks including matrices, vectors, metadata, and error messages.

This document describes the full UI workflow, execution pipeline, and practical recommendations for each numerical method.

---

## 2. UI Workflow

The complete workflow follows this pattern:

```
Select calculation type → Select method → Choose input mode → Provide A (and b) → Run → View results
```

Each step is described in detail below.

---

## 3. Step 1 — Select Calculation Type

The user chooses between:

| Type | Description |
|------|-------------|
| **Matrix Operations** | Operations on a single matrix A |
| **System of Equations** | Solving Ax = b using direct or iterative methods |

This selection determines:

- Available methods  
- Required inputs  
- Validation rules  
- Output structure  

---

## 4. Step 2 — Select Method

The dropdown dynamically filters available methods based on the selected calculation type.

### **Matrix Operations**
| Method | Description |
|--------|-------------|
| Determinant | Scalar value det(A) |
| Inverse | Matrix A⁻¹ |
| Norm | ‖A‖ (default: 2‑norm) |
| Condition Number | κ(A) |
| Transpose | Aᵀ |
| Rank | rank(A) |

### **System Solvers**
| Method | Description |
|--------|-------------|
| Gauss | Forward elimination + back substitution |
| Gauss‑Jordan | Full row reduction |
| LU | Lower/Upper factorization |
| Cholesky | A = LLᵀ (SPD matrices) |
| QR | Orthogonal factorization |
| Jacobi | Iterative solver |
| Gauss‑Seidel | Iterative solver |

The selected method determines:

- Whether vector `b` is required  
- Whether the matrix must be square  
- Whether the matrix must be symmetric (Cholesky)  
- Whether iterative parameters apply (Jacobi / GS)  

---

## 5. Step 3 — Choose Input Mode

The module supports two input modes:

### **Upload Mode (default)**

Accepts:

- `.txt` — matrix or system of equations  
- `.csv` — matrix  
- `.xlsx` — matrix  

TXT files may contain:

```
1 2 3
4 5 6
7 8 9
```

or linear systems:

```
3x + 2y - z = 5
x - y + 5z = 2
```

The parser automatically detects:

- variables  
- coefficients  
- right‑hand side vector  
- matrix shape  

### **Table Mode**

The user manually enters:

- Matrix A (editable table)  
- Vector b (only for systems)  

This mode is ideal for quick testing or small examples.

---

## 6. Step 4 — Data Loading

Depending on the input mode, the module constructs:

### **Matrix A**
Always required.

### **Vector b**
Required only for system solvers.

### **TXT System Parsing**
The parser extracts:

- variables in alphabetical order  
- coefficients for each variable  
- right‑hand side values  

Example:

```
3x + 2y = 5
x - y = 1
```

Produces:

```
A = [[3, 2],
     [1, -1]]

b = [5, 1]
```

---

## 7. Step 5 — Run Linear Algebra

When the user clicks **Run**, the callback:

1. Reads A and b from table or upload  
2. Validates the input using `LinearAlgebraValidator`  
3. Executes the method using `LinearAlgebraExecutor`  
4. Normalizes the result using `Renderer`  
5. Builds UI blocks using `UIContract`  
6. Renders the final output in `linear-algebra-result-area`  

---

## 8. Rendered Results

The dynamic result area displays **independent blocks**, depending on the method and output.

### 8.1 Scalar Result
For determinant, norm, condition number, rank.

Rendered as Markdown:

```
Result: ⧼value⧽
```

---

### 8.2 Matrix Result
For inverse, transpose, LU, QR, Cholesky.

Rendered using:

- `dash_table.DataTable`  
- matrix group blocks (for factorizations)  

---

### 8.3 Vector Result
For system solvers:

```
x = [ ... ]
```

---

### 8.4 Error Blocks
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

- `linear_algebra_callbacks.py` — UI logic  
- `_build_dataframe_from_upload()` — file parsing  
- `_parse_linear_system_txt()` — TXT equation parsing  
- `NumericalMethod` — orchestration  
- `LinearAlgebraValidator` — validation  
- `LinearAlgebraExecutor` — numerical computation  
- `Renderer` — payload normalization  
- `UIContract` — block construction  
- `result_view.py` — final rendering  

---

## 10. Practical Recommendations per Method

Different methods have different stability and performance characteristics.

### **Determinant**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 200×200 |
| Notes | Uses LU internally; stable for large matrices |

---

### **Inverse**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 150×150 |
| Notes | Avoid in iterative contexts; prefer solving Ax=b |

---

### **Norm**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 300×300 |
| Notes | Very stable |

---

### **Condition Number**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 150×150 |
| Notes | Sensitive to ill‑conditioned matrices |

---

### **Rank**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 300×300 |
| Notes | Uses SVD; stable but expensive |

---

### **LU / Cholesky / QR**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 200×200 |
| Notes | Factorizations are stable and fast |

---

### **Gauss / Gauss‑Jordan**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 150×150 |
| Notes | Gauss‑Jordan is slower; Gauss preferred |

---

### **Jacobi / Gauss‑Seidel**
| Property | Recommendation |
|---------|----------------|
| Matrix size | Up to 100×100 |
| Notes | Require diagonally dominant matrices |

---

## 11. Example Usage

1. Select **System of Equations**  
2. Select **LU**  
3. Choose **Upload Mode**  
4. Upload:

```
3x + 2y = 5
x - y = 1
```

5. Click **Run**

The system will display:

- L and U matrices  
- solution vector  
- metadata  

---

## 12. Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ConstructionError` | ragged matrix | ensure rectangular shape |
| `ValidationError` | missing b | provide vector b |
| `ExecutionError` | singular matrix | use pseudo‑inverse or adjust input |
| `ParsingError` | malformed TXT system | correct equation syntax |

---

## 13. Extending the Module

To add a new linear algebra method:

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

