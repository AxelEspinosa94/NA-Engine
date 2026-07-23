
---

# NA‑Engine — Linear Algebra Module (Backend Documentation)

This document describes the backend implementation of the Linear Algebra module in NA‑Engine.  
It covers the constructor, validator, executor, and an example calculation for both matrix operations and linear system solvers.

Supported calculation modes:

### Matrix Operations
- `determinant`
- `inverse`
- `norm`
- `condition_number`
- `transpose`
- `rank`

### Linear System Solvers
- `gauss`
- `gauss_jordan`
- `lu`
- `cholesky`
- `qr`
- `jacobi`
- `gauss_seidel`

---

# I. Constructor (`LinearAlgebra`)

The constructor prepares and stores:

- Matrix **A** (required for all modes)
- Vector **b** (required only for system solvers)
- The selected `calculation_mode`

It does **not** perform validation or computation — it only prepares data for the validator and executor.

## 1. Matrix A

If provided:

```python
"A": [[...], [...], ...]
```

it is converted to a NumPy array:

```python
self.A = np.array(A, dtype=float)
```

## 2. Vector b (optional)

Only required for system solvers:

```python
"b": [...]
```

Stored as:

```python
self.b = np.array(b, dtype=float)
```

## 3. Calculation Mode

The constructor stores:

```python
self.calculation_mode = input_data.get("calculation_mode")
```

This determines which operation or solver will be executed.

---

# II. Validator (`LinearAlgebraValidator`)

The validator ensures that:

- Required fields exist  
- Matrix dimensions are correct  
- Method‑specific constraints are satisfied  

It validates **before** the constructor is used by the executor.

---

## 1. Required Fields

### `calculation_mode`
Must be provided.

### Matrix A
- Must exist  
- Must be 2‑dimensional  
- Must contain no NaN or infinity  

### Vector b (system solvers only)
Required for:

```
gauss, gauss_jordan, lu, cholesky, qr, jacobi, gauss_seidel
```

Must satisfy:

- 1‑dimensional  
- Length matches number of rows of A  

---

## 2. Square Matrix Requirements

The following modes require a square matrix:

- `determinant`
- `inverse`
- `lu`
- `cholesky`
- `qr`

Validator checks:

```python
if A.shape[0] != A.shape[1]:
    raise ValidationError(...)
```

---

## 3. Cholesky‑Specific Validation

Cholesky requires:

- Matrix must be symmetric  
- Matrix must be positive definite (checked implicitly during execution)

Validator checks symmetry:

```python
np.allclose(A, A.T)
```

---

# III. Executor (`LinearAlgebraExecutor`)

The executor performs the actual computation.  
It dispatches based on `calculation_mode`:

```python
dispatch = {
    "determinant": self.determinant,
    "inverse": self.inverse,
    ...
    "gauss": self.gauss,
    ...
}
```

Each method returns a dictionary containing the result.

---

# 1. Matrix Operations

### Determinant
Uses:

```python
np.linalg.det(A)
```

Returns:

```json
{ "determinant": value }
```

---

### Inverse

```python
np.linalg.inv(A)
```

---

### Norm

Matrix 2‑norm:

```python
np.linalg.norm(A)
```

---

### Condition Number

```python
np.linalg.cond(A)
```

---

### Transpose

```python
A.T
```

---

### Rank

```python
np.linalg.matrix_rank(A)
```

---

# 2. Linear System Solvers

## Gauss Elimination (with partial pivoting)

Steps:

1. Pivot selection  
2. Row swapping  
3. Forward elimination  
4. Back substitution  

Returns:

```json
{ "solution": x }
```

---

## Gauss‑Jordan Elimination

Builds augmented matrix `[A | b]`, performs:

- Pivoting  
- Row normalization  
- Row elimination  

Returns:

```json
{ "solution": x }
```

---

## LU Decomposition (manual, with partial pivoting)

Produces:

\[
PA = LU
\]

Then solves:

- \( Ly = Pb \)  
- \( Ux = y \)

Returns:

```json
{ "solution": x, "L": L, "U": U, "P": P }
```

---

## Cholesky Factorization

Requires symmetric positive‑definite matrix.

\[
A = LL^T
\]

Solves:

- \( Ly = b \)  
- \( L^T x = y \)

---

## QR Decomposition

\[
A = QR
\]

Solves:

- \( y = Q^T b \)  
- \( Rx = y \)

---

## Jacobi Iteration

Iterative solver:

\[
x_i^{(k+1)} = \frac{1}{A_{ii}} \left(b_i - \sum_{j\neq i} A_{ij} x_j^{(k)}\right)
\]

Stops when:

\[
\|x^{(k+1)} - x^{(k)}\| < tol
\]

---

## Gauss‑Seidel Iteration

Uses updated values immediately:

\[
x_i^{(k+1)} = \frac{1}{A_{ii}}
\left(b_i - \sum_{j<i} A_{ij} x_j^{(k+1)} - \sum_{j>i} A_{ij} x_j^{(k)}\right)
\]

Converges faster than Jacobi.

---

# IV. Example Calculation (LU Decomposition)

Example input:

```python
from core.base_method import NumericalMethod

method = NumericalMethod(
    method="linear_algebra",
    input_data={
        "calculation_mode": "lu",
        "A": [[4, 3], [6, 3]],
        "b": [10, 12]
    }
)

method.validate_input()
result = method.execute()
```

### Expected Output

LU decomposition yields:

\[
x = [1, 2]
\]

### Example Result Structure

```json
{
  "status": "success",
  "result": {
    "solution": [1.0, 2.0],
    "L": [...],
    "U": [...],
    "P": [...]
  }
}
```

---

# End of Document

---

