
---

# NA‑Engine — Development Checklist (DEV)

This checklist defines all required steps before promoting any work from
feature/bug/fix branches into the `dev` environment.  
It ensures code quality, stability, and consistency across modules.

---

# 1. Branch Requirements

- [ ] Work is done in a dedicated branch:
  - `feature/<name>`
  - `bug/<module>/<description>`
  - `fix/<description>`
- [ ] Branch created from `dev`
- [ ] Branch name follows naming conventions
- [ ] Branch contains only changes relevant to the issue/feature

---

# 2. Coding Standards

- [ ] Code compiles and runs locally
- [ ] No debug prints (`print`, `logger.debug`, etc.)
- [ ] No commented-out code left behind
- [ ] Follows project style guidelines (naming, structure, clarity)
- [ ] Follows Conventional Commits for all commits
- [ ] No duplicated logic introduced
- [ ] No architectural violations (executor → renderer → UIContract)

---

# 3. Module Validation

Validate the module you worked on:

- [ ] Core functionality works as expected
- [ ] Edge cases tested
- [ ] Invalid inputs handled gracefully
- [ ] Numerical correctness validated
- [ ] Renderer outputs correct blocks:
  - Value block
  - Expression block
  - Table block (if applicable)
  - Plot block (if applicable)
- [ ] UIContract dispatch consistent

---

# 4. Unit Tests

- [ ] New unit tests added for new logic
- [ ] Existing tests updated if needed
- [ ] All unit tests pass:
  ```bash
  pytest -q
  ```

---

# 5. Stress Tests

- [ ] Stress tests relevant to the module pass:
  ```bash
  pytest tests/stress -vv -s
  ```
- [ ] No performance regressions introduced
- [ ] No infinite loops or excessive recursion
- [ ] No memory spikes

---

# 6. Integration Tests

Validate that your changes do not break other modules:

- [ ] Interpolation still works
- [ ] Derivatives still work
- [ ] Linear algebra still works
- [ ] Nonlinear equations still work
- [ ] Renderers still produce consistent output
- [ ] UIContract dispatch unaffected

---

# 7. Documentation

- [ ] Docstrings updated
- [ ] Markdown documentation updated (if applicable)
- [ ] CHANGELOG entry drafted (not final)
- [ ] Examples updated (if applicable)

---

# 8. Self‑Review

- [ ] Code is readable and maintainable
- [ ] No unnecessary complexity
- [ ] No unrelated changes included
- [ ] No leftover experimental code
- [ ] Branch is up-to-date with `dev`:
  ```bash
  git pull origin dev
  ```

---

# 9. Create Pull Request to `dev`

- [ ] PR created with clear description
- [ ] PR linked to issue/ticket
- [ ] PR follows PULL_REQUEST_TEMPLATE
- [ ] CI/CD pipeline passes
- [ ] PR ready for review

---

# ✔ DEV Stage Completed

---

