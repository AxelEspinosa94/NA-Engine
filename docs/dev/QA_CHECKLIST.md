
---

# NA‑Engine — Quality Assurance Checklist (QA)

This checklist defines all required validation steps before promoting code
from the `qa` environment into `main` (production).  
QA ensures that NA‑Engine is stable, correct, performant, visually consistent,
and ready for release.

---

# 1. Branch Requirements

- [ ] PR source is `dev`
- [ ] PR target is `qa`
- [ ] Branch contains only changes intended for this release
- [ ] Branch is up-to-date with `qa`
  ```bash
  git pull origin qa
  ```

---

# 2. Functional Testing

Validate full functionality of the module(s) affected:

- [ ] Core functionality works as expected
- [ ] All supported input types tested
- [ ] Special functions tested (sin, cos, exp, log, tan, etc.)
- [ ] Composite expressions tested (nested functions, chained operations)
- [ ] Boundary values tested (large limits, negative limits, small intervals)
- [ ] Error handling validated (invalid inputs, malformed expressions)

---

# 3. Regression Testing

Ensure no other module was broken by recent changes:

- [ ] Integration module regression tests pass
- [ ] Interpolation module regression tests pass
- [ ] Derivatives module regression tests pass
- [ ] Linear algebra module regression tests pass
- [ ] Nonlinear equations module regression tests pass
- [ ] Renderers produce correct blocks across all modules
- [ ] UIContract dispatch remains consistent

---

# 4. Performance Testing

Validate that performance remains acceptable:

- [ ] No new bottlenecks introduced
- [ ] No excessive recursion or loops
- [ ] No memory spikes
- [ ] Stress tests pass:
  ```bash
  pytest tests/stress -vv -s
  ```

---

# 5. Stability Testing

Validate robustness under extreme or unusual conditions:

- [ ] Very large inputs tested
- [ ] Very small inputs tested
- [ ] Highly oscillatory functions tested
- [ ] Discontinuous functions tested
- [ ] Randomized inputs tested
- [ ] No crashes or unhandled exceptions

---

# 6. UI/UX Validation

Ensure visual and interactive consistency:

- [ ] Renderer blocks display correctly:
  - Value block
  - Expression block
  - Table block
  - Plot block
- [ ] LaTeX renders correctly
- [ ] Tooltips display correct information
- [ ] Theme consistency (light/dark)
- [ ] No layout breaks or spacing issues

---

# 7. Integration Between Modules

Validate cross-module interactions:

- [ ] Parser works correctly with all modules
- [ ] Executor handles outputs from other modules
- [ ] Renderer handles mixed-module outputs
- [ ] UIContract routes results correctly

---

# 8. Security & Sanitization

Validate input safety:

- [ ] Parser rejects unsafe expressions
- [ ] No code injection possible
- [ ] No unsafe Python evaluation paths
- [ ] Invalid characters handled gracefully

---

# 9. Documentation & Release Preparation

- [ ] CHANGELOG updated and finalized
- [ ] Version bump confirmed
- [ ] Documentation updated (if applicable)
- [ ] Release notes drafted
- [ ] Examples updated (if applicable)

---

# 10. CI/CD Validation

- [ ] GitHub Actions pipeline passes for `qa`
- [ ] All tests green
- [ ] No warnings or errors in logs
- [ ] PR follows PULL_REQUEST_TEMPLATE

---

# 11. Approval

- [ ] QA reviewer approves (self-approval allowed if solo)
- [ ] PR ready for promotion to `main`

---

# ✔ QA Stage Completed — Ready for Production

---

