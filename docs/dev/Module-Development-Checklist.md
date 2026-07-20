
---

# 📋 **NA‑Engine — Module Development Checklist**  
*Standardized checklist for implementing any numerical module in NA‑Engine.*

This checklist ensures consistency across all modules and accelerates development by following the same architectural, UI, backend, testing, and documentation patterns.

---

---

# 🟦 0. Backend — Constructor, Validator, Executor

### Constructor
- [ ] Parse all fields from `input_data`
- [ ] Handle input mode (table / function / upload)
- [ ] Raise `ConstructionError` for malformed input

### Validator
- [ ] Validate each `calculation_mode`
- [ ] Add `_validate_<method>()` if rules differ
- [ ] Reuse `_validate_default()` when possible
- [ ] Raise `ValidationError` with descriptive messages

---
# 🟦 1. Executor - Output Design

- [ ] Implement `_run_<method>()`
- [ ] Return standardized dict (see section 2)
- [ ] Generate symbolic expressions if applicable
- [ ] Generate plot data (`x`, `y`, nodes)
- [ ] Raise `ExecutionError` on failure

Define what the module should display:

- [ ] Scalar value  
- [ ] Expression / formula  
- [ ] Plot (curve, nodes, trajectories, comparison)  
- [ ] Table (iterations, nodes, steps)  
- [ ] Vector / matrix (systems, LU, Jacobians)

Renderer <module>:

- [ ] Check `Renderer.KEY_DISPATCH`  
- [ ] Add new payload types if needed  
- [ ] Define executor return structure:
  ```python
  {
      "value": float,
      "expression": str,
      "table": pd.DataFrame,
      "x": list[float],
      "y": list[float],
      "matrix": list[list[float]],
      "vector": list[float],
  }
  ```
- [ ] If composite output:
  - [ ] Define block order explicitly  
  - [ ] Ensure `UIContract._build_blocks()` supports all keys  

### Error Normalization
- [ ] Ensure all errors pass through `ErrorNormalizer`

---
# 🟦 2. Smoke Test

Create a minimal end‑to‑end test to confirm the module is “alive” before writing full tests.

- [ ] Create `scripts/smoke_<module>.py`
- [ ] Build a minimal `input_data` dict
- [ ] Run:
  ```python
  nm = NumericalMethod(<"module">, input_data)
  nm.validate_input()
  outcome = nm.execute()
  payload = UIContract().resolve(method, outcome)
  ```
- [ ] Confirm:
  - [ ] `outcome["status"] == "success"`
  - [ ] Renderer returns correct payload types
  - [ ] UIContract returns a non‑empty `html.Div`

---

# 🟦 3. UI Setup

- [ ] Identify all required inputs for the module:
  - method selector  
  - input mode (table / function / upload)  
  - module‑specific parameters (`xk`, `a`, `b`, `n`, `tol`, `max_iter`, etc.)
- [ ] Reuse existing CSS classes:
  - `.card`, `.input`, `.btn-primary`, `.upload-area`, `.result-area`, `.dark`
- [ ] If new styles are needed:
  - base them on interpolation module  
  - place them in `app/assets/<module>.css` 
  - include `.dark` overrides
- [ ] Build layout in `app/layout/<module>_layout.py`:
  - [ ] Module header (`.module-header`)
  - [ ] Method selector (`dcc.Dropdown`)
  - [ ] Input mode selector (`dcc.RadioItems`) if applicable
  - [ ] Dynamic input area (`html.Div(id="<module>-input-area")`)
  - [ ] Parameter cards (`xk`, `a`, `b`, `n`, `tol`, etc.)
  - [ ] Execute button (`.btn-primary`)
  - [ ] Result area (`html.Div(id="<module>-result-area")`)
- [ ] Register layout in `app/layout/base_layout.py`
- [ ] Enable navbar button for the module
- [ ] Enable home banner/card navigation
- [ ] Run the module UI manually in the browser
- [ ] Confirm dynamic input area loads correctly

---

# 🟦 4. Callbacks

- [ ] Create `app/callbacks/<module>_callbacks.py`
- [ ] Instantiate:
  ```python
  contract = UIContract()
  ```

### build_input_area
- [ ] Triggered by method selector + input mode
- [ ] Calls `_build_mode_area(method, mode)`
- [ ] Shows/hides parameter cards
- [ ] Uses `dash.no_update` when appropriate

### run_<module>
- [ ] Read all `State` inputs
- [ ] Build `input_data`
- [ ] Catch `ValidationError` before execution
- [ ] Call `NumericalMethod`
- [ ] Call `contract.resolve(method, outcome)`
- [ ] Return result to `<module>-result-area`

### Optional callbacks
- [ ] `add_row` for editable tables  
- [ ] `_build_dataframe_from_upload()` for upload mode  

### Registration
- [ ] Add to `app/app.py`:
  ```python
  register_<module>_callbacks(app)
  ```

---

# 🟦 5. Testing & CI

### Stress Tests (`tests/stress/test_<module>_stress.py`)
- [ ] Volume: large datasets (50–500+ nodes/steps)  
- [ ] Precision: analytical ground truth  
- [ ] Stability: determinism  
- [ ] Error handling: invalid formats  
- [ ] Upload tests: CSV/TXT/Excel/JSON  (if apply)
- [ ] Full pipeline: upload/table → NumericalMethod → UIContract → html.Div  
- [ ] Mark as `@pytest.mark.pending` until module is complete  

### CI
- [ ] Confirm GitHub Actions passes  

---

# 🟦 6. Documentation

- [ ] Update `docs/arch/overview.md` if architecture changed  
- [ ] Update theory docs in `docs/theory/<module>.md`:
  - formulas  
  - derivations  
  - stability conditions  
  - analytical examples  

---

# 🟦 Reference Module: Interpolation

Use interpolation as the baseline for:

- layout  
- callbacks  
- upload mode  
- DataFrame construction  
- stress tests  
- documentation structure  

Files to reference:

```
app/layout/interpolation_layout.py
app/callbacks/interpolation_callbacks.py
tests/stress/test_interpolation_stress.py
tests/stress/test_interpolation_upload.py
docs/UI/interpolation/
```

---
# Log:

**07/07/2026**: Steps were reordered to match the current work done in Interpolation and Integration module.
**07/16/2026**: Executor step was isolated in step 1 since it needs special preparation for the output.

---