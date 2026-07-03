# Module Development Checklist

Standardized checklist for implementing a new numerical module in NA-Engine.
Follow this order to ensure consistency across all modules.

---

## 1. UI Setup

- [ ] Identify all required inputs for the module (method selector, input mode,
      specific parameters like `xk`, `a`, `b`, `n`, tolerance, etc.)
- [ ] Check existing CSS classes before writing new styles —
      reuse `.card`, `.input`, `.btn-primary`, `.upload-area`, `.result-area`, etc.
- [ ] If new styles are needed, base them on an existing functional module
      (interpolation is the reference) and add them to a dedicated
      `app/assets/<module>.css` file following the `.dark` override pattern
- [ ] Build the layout in `app/layout/<module>_layout.py`:
  - [ ] Module header (`.module-header`)
  - [ ] Method selector (`dcc.Dropdown`)
  - [ ] Input mode selector (`dcc.RadioItems`: table / function / upload)
      when applicable
  - [ ] Dynamic input area (`html.Div(id="<module>-input-area")`)
  - [ ] Method-specific parameter inputs (e.g. `xk`, `a`, `b`, `n`)
  - [ ] Execute button (`.btn-primary`)
  - [ ] Result area (`html.Div(id="<module>-result-area", className="result-area")`)
- [ ] Register the layout section in `app/layout/base_layout.py`
- [ ] Enable the navbar button for the module in `base_layout.py`
- [ ] Enable the home banner/card that navigates to the module

---

## 2. Output Design

- [ ] Define what results the module should display:
  - [ ] Scalar value (e.g. integral result, derivative value)
  - [ ] Expression / formula
  - [ ] Plot (curve, nodes, comparison)
  - [ ] Table (iteration table, node table)
  - [ ] Vector / matrix (for linear systems, LU decomposition, etc.)
- [ ] Check `Renderer.KEY_DISPATCH` — verify the executor output keys
      map to the correct payload type, or add new entries if needed
- [ ] Define the executor return dict structure:
  ```python
  {
      "value":      float,        # main numerical result
      "expression": str,          # symbolic or formatted expression (if applicable)
      "table":      pd.DataFrame, # iteration or node table (if applicable)
      "x":          list[float],  # x points for plotting (if applicable)
      "y":          list[float],  # y points for plotting (if applicable)
  }
  ```
- [ ] If the result is composite (multiple blocks), verify `UIContract._build_blocks()`
      covers the new keys or add new branches as needed

---

## 3. Backend — Constructor, Validator, Executor

- [ ] Verify the constructor exists and parses `input_data` correctly:
  - [ ] Assigns all required attributes from `input_data`
  - [ ] Handles `mode` (table / function / upload) if applicable
  - [ ] Raises `ConstructionError` for structurally invalid inputs
- [ ] Verify the validator covers all `calculation_mode` values:
  - [ ] Add `_validate_<mode>()` per method if rules differ
  - [ ] Reuse `_validate_default()` if methods share the same rules
  - [ ] Raises `ValidationError` with descriptive messages
- [ ] Implement or update `_run_<method>()` in the executor:
  - [ ] Returns the standardized result dict defined in step 2
  - [ ] Adds symbolic expression generation if needed
  - [ ] Adds plot data generation (`x`, `y`, `x_nodes`, `y_nodes`) if needed
  - [ ] Raises `ExecutionError` on computation failure
- [ ] Register the module in `core/method_catalog.json`:
  ```json
  {
    "<method>": {
      "classConstructor":    "core.<module>.<module>.<Module>",
      "classInputValidator": "strategies.validators.<module>_validators.<Module>Validator",
      "classExecutor":       "strategies.executors.<module>_executors.<Module>Executor"
    }
  }
  ```

---

## 4. Callbacks

- [ ] Create `app/callbacks/<module>_callbacks.py`
- [ ] Instantiate `UIContract` as a module-level global:
  ```python
  contract = UIContract()
  ```
- [ ] Implement `build_input_area` callback:
  - [ ] Triggered by method selector + input mode selector
  - [ ] Returns dynamic form components via `_build_mode_area(method, mode)`
  - [ ] Shows/hides parameter cards (xk, a/b, n, etc.) as needed
- [ ] Implement `run_<module>` callback:
  - [ ] Reads all `State` inputs
  - [ ] Builds `input_data` dict
  - [ ] Handles `ValidationError` before calling `execute()`
  - [ ] Calls `contract.resolve(method, outcome)`
  - [ ] Returns result to `Output("<module>-result-area", "children")`
- [ ] Implement `add_row` callback if the module uses an editable `DataTable`
- [ ] Implement `_build_dataframe_from_upload()` if upload mode is supported
- [ ] Register callbacks in `app/app.py`:
  ```python
  from app.callbacks.<module>_callbacks import register_<module>_callbacks
  register_<module>_callbacks(app)
  ```

---

## 5. Testing & CI

- [ ] **Unit tests** — `tests/unit/test_<module>.py`:
  - [ ] Test constructor with valid and invalid inputs
  - [ ] Test validator for each `calculation_mode`
  - [ ] Test executor return structure for each method
  - [ ] Test `Renderer` payload type for each result key

- [ ] **Integration tests** — `tests/integration/test_<module>.py`:
  - [ ] Happy path: valid input → `status == "success"`
  - [ ] Error path: invalid input → `ValidationError` handled cleanly
  - [ ] Edge cases per method (see interpolation as reference)
  - [ ] `UIContract.resolve()` returns `html.Div` for both success and error

- [ ] **Stress tests** — `tests/stress/test_<module>_stress.py`:
  - [ ] Volume: large datasets (50, 200, 500+ nodes/steps)
  - [ ] Precision: known analytical results with tolerance by method
  - [ ] Stability: determinism (same input → same output across runs)
  - [ ] Error handling: invalid files, missing columns, unsupported formats
  - [ ] Upload: all supported formats (CSV, TXT, Excel, JSON) if applicable
  - [ ] Full process: upload/table → `NumericalMethod` → `UIContract` → `html.Div`
  - [ ] Mark tests as `@pytest.mark.pending` until the module is complete,
        then remove the marker to include them in CI automatically

- [ ] **CI verification**:
  - [ ] Push to `main` or `develop` and confirm GitHub Actions passes
  - [ ] Check the Actions tab for green status
  - [ ] Update stress test matrix in `docs/UI/stress_testing_strategy.md`

---

## 6. Documentation

- [ ] Update `core/method_catalog.json` entry (already done in step 3)
- [ ] Update `docs/arch/overview.md` if new architectural patterns were introduced
- [ ] Add module entry to the stress test matrix in
      `docs/UI/stress_testing_strategy.md` and mark as `✓ Done`
- [ ] Create `docs/UI/<module>/ui_evidence.md` with:
  - [ ] Sample input used for manual testing
  - [ ] Outcome dict from smoke test
  - [ ] Rendered payload type
  - [ ] Expected vs actual result (analytical ground truth where available)
  - [ ] Screenshot or smoke test output (optional)
- [ ] Run smoke test and confirm output:
  ```bash
  python scripts/smoke_<module>.py
  ```

---

## Reference: Interpolation as Baseline

Interpolation is the reference implementation for all modules.
When in doubt about structure, naming, or patterns, check:

```
app/layout/interpolation_layout.py
app/callbacks/interpolation_callbacks.py
tests/stress/test_interpolation_stress.py
tests/stress/test_interpolation_upload.py
docs/UI/interpolation/
```