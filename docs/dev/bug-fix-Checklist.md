
---

# ✅ **Bug Fix Checklist — Integration Module (DevOps Workflow)**

# Bug Fix Checklist — Integration Module (DevOps Workflow)

This checklist describes the full DevOps workflow for fixing the bug in the
Numerical Integration module where trigonometric and exponential functions
are not being recognized due to non‑`x` characters in the parser.

---

## 1. Create the Bug Branch

- [ ] Switch to `develop`  
  ```bash
  git checkout develop
  git pull
  ```

- [ ] Create a dedicated bug branch  
  ```bash
  git checkout -b bug/integration/functions_unrecognized
  ```

- [ ] Confirm the branch name follows the project’s naming conventions  
  (`bug/<module>/<short-description>`)

---

## 2. Reproduce the Bug

- [ ] Run the integration module with:
  - `sin(t)`
  - `cos(u)`
  - `exp(z)`
  - Any function using a variable other than `x`

- [ ] Confirm the failure mode:
  - Incorrect parsing
  - Wrong variable binding
  - Function not evaluated
  - Integration returning `None`, `0`, or raising an exception

---

## 3. Fix the Bug

- [ ] Update the parser to accept arbitrary variable names  
- [ ] Normalize variable names internally (e.g., map to `x`)  
- [ ] Ensure the executor receives the correct callable  
- [ ] Add support for:
  - Trigonometric functions
  - Exponential functions
  - Logarithmic functions
  - Any other functions used in NA‑Engine

- [ ] Add unit tests for:
  - `sin(t)`
  - `exp(z)`
  - `cos(u)`
  - Mixed expressions (e.g., `exp(t) * sin(t)`)

---

## 4. Validate the Fix

- [ ] Run all integration methods:
  - Trapezoid (simple/composite)
  - Simpson 1/3
  - Simpson 3/8 (if present)
  - Future methods (Clenshaw–Curtis, Monte Carlo, Adaptive Quadrature)

- [ ] Confirm correct numerical results  
- [ ] Confirm renderer outputs:
  - Value block
  - Expression block
  - Table block (if applicable)
  - Plot block (if applicable)

---

## 5. Commit and Push

- [ ] Stage changes  
  ```bash
  git add .
  ```

- [ ] Commit using Conventional Commits  
  ```bash
  git commit -m "fix(integration): allow arbitrary variable names in integrand parsing"
  ```

- [ ] Push the branch  
  ```bash
  git push origin bug/integration/functions_unrecognized
  ```

---

## 6. Create a Merge Request (Pull Request)

- [ ] Open a PR from  
  `bug/integration/functions_unrecognized` → `main`

- [ ] Fill out the PR template:
  - Summary of the bug
  - Explanation of the fix
  - Tests added
  - Modules affected
  - Screenshots (optional)

- [ ] Self‑review the PR:
  - Code clarity
  - No leftover debug prints
  - No unrelated changes
  - Renderer/UIContract consistency

---

## 7. Merge to Main

> **Note:** Even if you are the only contributor, the project requires PRs to merge into `main` to avoid ambiguity and enforce a clean workflow.

- [ ] Ensure branch protection rules are active:
  - Prevent direct pushes to `main`
  - Require PRs for merging
  - (Optional) Require approvals (you can approve your own PR)

- [ ] Use **Squash and Merge**  
  This keeps the commit history clean.

---

## 8. Release the Fix

- [ ] Update `CHANGELOG.md`  
- [ ] Run the Makefile release command  
  ```bash
  make release-patch
  ```

- [ ] Verify the new tag was created and pushed  
- [ ] Confirm the version appears correctly in the NA‑Engine header

---

## 9. Close the Ticket

- [ ] Link the PR to the issue  
- [ ] Mark the bug as resolved  
- [ ] Add notes for future maintainers (optional)

---

# ✔ Bug Fix Workflow Completed

---
