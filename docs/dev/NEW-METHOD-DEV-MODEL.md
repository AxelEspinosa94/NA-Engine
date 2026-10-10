
---

# ✅ **NA‑Engine — Method Integration Checklist**  
### *Standard Procedure for Adding New Numerical Methods*  
*(Version 1.0 — evolving document)*


---

## 1. Preparation
- Identify the new numerical method to integrate.
- Review mathematical theory and required inputs.
- Create or update the theoretical notes for the method.
- Ensure the method fits into an existing module (e.g., integration, ODEs, interpolation).

---

## 2. Theory Documentation
- Create `theory/theory_clenshaw_curtis.md`.
- Include:
  - Introduction
  - Chebyshev transformation
  - Cosine expansion
  - Node generation
  - Weight computation
  - Final quadrature formula
  - Examples
- Ensure Markdown is compatible with NA-Engine’s documentation renderer.

---

## 3. Validator Implementation
- Create a validator file:
  - `validators/integration/clenshaw_curtis_validator.py`
- Validate:
  - domain constraints
  - required inputs
  - types and ranges
- Ensure validator raises `ValidationError` on failure.

---

## 4. Executor Implementation
- Create a new file under the module directory:
  - `executors/integration/clenshaw_curtis.py`
- Implement the method in an isolated class.
- Follow the standard executor interface:
  - `__init__(input_data)`
  - `validate_input()` (optional if validator is separate)
  - `execute()`
- Ensure the executor returns a result dictionary consistent with NA-Engine conventions.

---

## 5. UI Integration
- Update the module dropdown to read from `method_catalog.json`.
- Ensure the new method appears automatically.
- Add dynamic input fields based on catalog metadata.
- Add tooltips from catalog metadata.
- Ensure the documentation panel loads the correct `.md` file.

---

## 6. Renderer & Contract Compatibility
- Verify the executor output matches renderer expectations.
- Ensure renderer produces correct blocks:
  - scalar
  - table
  - plot (if applicable)
- Ensure UIContract maps blocks to Dash components correctly.

---

## 7. Testing
### 7.1 Unit Tests
- Test the executor logic in isolation.
- Test validator behavior.
- Test edge cases and invalid inputs.

### 7.2 Stress Tests
- Run the full pipeline:
  - Constructor → Validator → Executor → Renderer → Contract
- Ensure the pipeline does not crash.
- Validate performance for large `n`.

### 7.3 Integration Tests
- Run the full pipeline and verify:
  - correctness of numerical result
  - correctness of rendered output
  - correctness of UIContract mapping
- Compare numerical output against known analytical results.

---

## 8. Migration Workflow
- Commit changes to feature branch.
- Open PR to `qa`.
- Run CI/CD tests.
- After approval, merge to `main`.

---

## 9. Release Procedure
- Update version number (minor release in clenshaw-curtis case, patch release in the others).
- Generate release notes:
  - new method added
  - architectural changes
  - documentation updates
  - new tests
- Tag release:
  - `vX.Y.Z`

---

## 10. Post-Release
- Update README and CHANGELOG if necessary.
- Update documentation index.
- Add examples to sample notebooks.
- Add method to future roadmap if extensions are planned.

---

## Notes
- This checklist evolves as NA-Engine grows.
- Major architectural changes should update this document.
- All new methods must follow this procedure for consistency.


---

