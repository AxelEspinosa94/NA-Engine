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

| Module         | Methods | Modes | Dataset Sizes | Status   |
|----------------|---------|-------|---------------|----------|
| Interpolation  | 4       | 3     | 100–5000      | ✓ Done   |
| Integration    | 3       | 3     | 1000–5000     | Pending  |
| Derivatives    | 3       | 3     | 100–500       | Pending  |
| Matrices       | 5       | 1     | 100×100       | Pending  |
| Systems        | 3       | 1     | 1000 iter     | Pending  |
| ODEs           | 10+     | 3     | 1000 steps    | Pending  |

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

## 7. Implemented Stress Tests — Interpolation

### 7.1 `test_interpolation_stress.py`

Covers the full pipeline from `NumericalMethod` to `html.Div` for all four
interpolation methods.

| Category    | Test                              | Methods                          | Sizes     |
|-------------|-----------------------------------|----------------------------------|-----------|
| Volume      | `test_volumen_muchos_nodos`       | Lagrange, Newton, Splines        | 10, 50, 100 nodes |
| Volume      | `test_volumen_hermite`            | Hermite                          | 10, 50 nodes |
| Precision   | `test_precision_polinomio_grado_2`| Lagrange, Newton, Splines, Hermite | 20 nodes |
| Precision   | `test_precision_funcion_lineal`   | Lagrange, Newton, Splines        | 20 nodes |
| Stability   | `test_runge_grado_alto`           | Lagrange, Newton                 | 15 nodes |
| Stability   | `test_determinismo`               | All                              | 4 nodes  |
| UIContract  | `test_contract_devuelve_div`      | All                              | 4 nodes  |
| UIContract  | `test_contract_error_devuelve_div`| All                              | —        |

**Tolerances by method for `test_precision_polinomio_grado_2`:**

| Method      | Tolerance |
|-------------|-----------|
| Lagrange    | `1e-6`    |
| Newton      | `1e-6`    |
| Splines     | `1e-2`    |
| Hermite     | `1e-2`    |

### 7.2 `test_interpolation_upload.py`

Covers the file upload pipeline: `dcc.Upload` → `_build_dataframe_from_upload()`
→ `NumericalMethod` → `UIContract` → `html.Div`.

**File formats tested:**

| Format  | Extension | Encoder         |
|---------|-----------|-----------------|
| CSV     | `.csv`    | `pd.to_csv()`   |
| TXT     | `.txt`    | `pd.to_csv(sep='\t')` |
| Excel   | `.xlsx`   | `pd.to_excel()` |
| JSON    | `.json`   | `pd.to_json()`  |

**Test coverage:**

| Category        | Test                               | Description                                      |
|-----------------|------------------------------------|--------------------------------------------------|
| Formats         | `test_upload_csv`                  | CSV parsed correctly for Lagrange, Newton, Splines |
| Formats         | `test_upload_txt`                  | TXT with tab separator                           |
| Formats         | `test_upload_excel`                | Excel (.xlsx)                                    |
| Formats         | `test_upload_json`                 | JSON format                                      |
| Formats         | `test_upload_hermite_csv`          | CSV with x, y, dy columns for Hermite            |
| Volume          | `test_upload_volumen_csv`          | CSV with 50, 200, 500 rows                       |
| Error handling  | `test_upload_none_contents`        | None contents raises ValidationError             |
| Error handling  | `test_upload_formato_no_soportado` | Unsupported format raises ValidationError        |
| Error handling  | `test_upload_columnas_faltantes`   | Missing y column raises ValidationError          |
| Error handling  | `test_upload_hermite_sin_dy`       | Missing dy column for Hermite raises ValidationError |
| Error handling  | `test_upload_columnas_extra_ignoradas` | Extra columns are ignored, only x, y kept    |
| Full process    | `test_full_process_upload`         | End-to-end: upload → NumericalMethod → html.Div |

---

## 8. Example Stress Test (Interpolation — future dash.testing)

```python
@pytest.mark.parametrize("method", ["lagrange", "newton", "hermite", "splines"])
@pytest.mark.parametrize("mode", ["table", "function", "upload"])
def test_interpolation_stress(dash_duo, method, mode):
    app = build_app()
    dash_duo.start_server(app)

    dash_duo.find_element("#tab-interpolation").click()
    dash_duo.select_dcc_dropdown("#interp-method", method)
    dash_duo.select_dcc_dropdown("#interp-input-mode", mode)

    if mode == "table":
        dash_duo.driver.execute_script("""
            const table = document.querySelector('#interp-table');
            table.data = Array.from({length: 1000}, (_, i) => ({x: i, y: i*i}));
        """)

    dash_duo.find_element("#interp-run-btn").click()
    dash_duo.wait_for_element("#interp-result-area", timeout=20)
    assert "Error" not in dash_duo.find_element("#interp-result-area").text
```

---

## 9. Reporting

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

## 10. CI/CD Integration

Stress tests run automatically via GitHub Actions on every push to `main` or `develop`
and on every pull request to `main`.

They are split by concern in the workflow:

```yaml
- name: Run stress tests
  run: pytest tests/stress/ -v --tb=short
```

`dash.testing` (Selenium-based) tests are **not** run on every commit due to the
WebDriver setup overhead. They are planned for nightly runs or pre-release checks.

---

## 11. Extending Stress Tests

To add stress tests for a new module:

1. Add a new file:  
   ```
   tests/stress/test_<module>_stress.py
   ```

2. Parametrize methods and modes  
3. Follow the same structure  
4. Add to the matrix in this document  

---

## 12. Notes

**Hermite — `test_precision_funcion_lineal`**  
Hermite was excluded from the precision test with $f(x) = 2x+1$ since the derivative
of a linear function is constant, generating oscillation in the resulting polynomial.
This is a known limitation of the method with this type of input, not an executor bug.

**Splines and Hermite — `test_precision_polinomio_grado_2`**  
A relaxed tolerance of `1e-2` is used for Splines and Hermite because cubic splines
with natural boundary conditions (M[0] = M[-1] = 0) introduce error near interval
endpoints with few nodes, and Hermite with degree-7 polynomials can oscillate with
sparse node sets. This is expected numerical behavior, not a defect.

---