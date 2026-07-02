
---

# 📘 **NA‑Engine — Stress Testing Strategy**  

## 1. Purpose

The goal of stress testing in NA‑Engine is to validate the stability, performance, and scalability of the entire numerical analysis pipeline:

```
UI → Callbacks → NumericalMethod → Constructor → Validator → Executor → Renderer → UIContract → Dash Components
```

Stress tests ensure that:

- Large datasets do not crash the UI  
- Executors remain stable under heavy load  
- Rendering remains responsive  
- Memory usage stays within safe limits  
- The system behaves consistently across all modules  

---

## 2. Scope

Stress tests apply to **all six numerical modules**:

| Module         | Methods (examples)                     |
|----------------|----------------------------------------|
| Interpolation  | Lagrange, Newton, Hermite, Splines     |
| Integration    | Trapecio, Simpson, Romberg             |
| Derivatives    | Forward, Backward, Central             |
| Matrices       | LU, Cholesky, Gauss, Inverse           |
| Systems        | Gauss-Seidel, Jacobi, Newton           |
| ODEs           | Euler, Heun, RK2, RK4, RKF45, Adams    |

Each module may have:

- Multiple methods  
- Multiple input modes (table, function, upload)  
- Multiple output types (scalar, vector, matrix, plot, table, markdown)  

Stress tests must cover **all combinations**.

---

## 3. Tools

### ✔ `pytest`  
Base test runner.

### ✔ `dash.testing`  
Official Dash integration testing framework.  
Allows:

- launching the full app  
- interacting with UI elements  
- filling tables  
- uploading files  
- clicking buttons  
- waiting for results  
- measuring responsiveness  

### ✔ Optional: `pytest-benchmark`  
For performance metrics.

---

## 4. Stress Dimensions

Stress tests must vary across:

### 4.1 Dataset Size
- 100 nodes  
- 500 nodes  
- 1000 nodes  
- 5000 nodes  
- 10,000 nodes (upload mode)

### 4.2 Method Complexity
- Simple methods (Lagrange, Euler)  
- Heavy methods (Splines, RK4, LU, Cholesky)  

### 4.3 UI Responsiveness
- Time to render tables  
- Time to render plots  
- Time to update dynamic areas  

### 4.4 Memory Usage
- Large DataFrames  
- Large plots  
- Multiple blocks rendered simultaneously  

### 4.5 Error Handling
- Invalid files  
- Missing columns  
- Non-numeric data  
- Function evaluation errors  

---

## 5. Stress Test Matrix

| Module         | Methods | Modes | Dataset Sizes |
|----------------|---------|-------|---------------|
| Interpolation  | 4       | 3     | 100–5000      |
| Integration    | 3       | 3     | 1000–5000     |
| Derivatives    | 3       | 3     | 100–500       |
| Matrices       | 5       | 1     | 100×100       |
| Systems        | 3       | 1     | 1000 iter     |
| ODEs           | 10+     | 3     | 1000 steps    |

---

## 6. Stress Test Structure

Each stress test follows this pattern:

1. Start the Dash app  
2. Navigate to the module  
3. Select method  
4. Select input mode  
5. Load large dataset  
6. Execute calculation  
7. Wait for result  
8. Validate:
   - no crash  
   - no error  
   - UI remains responsive  
   - output is rendered  

---

## 7. Example Stress Test (Interpolation)

```python
@pytest.mark.parametrize("method", ["lagrange", "newton", "hermite", "splines"])
@pytest.mark.parametrize("mode", ["table", "function", "upload"])
def test_interpolation_stress(dash_duo, method, mode):
    app = build_app()
    dash_duo.start_server(app)

    # Navigate to module
    dash_duo.find_element("#tab-interpolation").click()

    # Select method
    dash_duo.find_element("#interp-method").click()
    dash_duo.select_dcc_dropdown("#interp-method", method)

    # Select mode
    dash_duo.select_dcc_dropdown("#interp-input-mode", mode)

    # Load large dataset (example for table mode)
    if mode == "table":
        dash_duo.driver.execute_script("""
            const table = document.querySelector('#interp-table');
            table.data = Array.from({length: 1000}, (_, i) => ({x: i, y: i*i}));
        """)

    # Execute
    dash_duo.find_element("#interp-run-btn").click()

    # Wait for result
    dash_duo.wait_for_element("#interp-result-area", timeout=20)

    # Validate
    assert "Error" not in dash_duo.find_element("#interp-result-area").text
```

---

## 8. Reporting

Each stress test must record:

- Execution time  
- Render time  
- Memory usage (optional)  
- Errors encountered  
- UI responsiveness  

Reports are stored in:

```
tests/reports/stress/
```

---

## 9. CI/CD Integration

Stress tests run:

- nightly  
- before releases  
- before merging large PRs  

They are **not** run on every commit due to cost.

---

## 10. Extending Stress Tests

To add stress tests for a new module:

1. Add a new file:  
   ```
   tests/stress/test_<module>_stress.py
   ```

2. Parametrize methods and modes  
3. Follow the same structure  
4. Add to the matrix in this document  

## 11. Notes

Hermite was excluded from the precision test  with $f(x)=2x+1$ since the derivative of this function is a constant, thus, generating oscilation in the resulting polynomial. This is a known limitation of the method with this type of input, not an executor's bug.

---
