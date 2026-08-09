
---

# Pull Request — NA‑Engine

Thank you for contributing to NA‑Engine.  
Please complete the following sections to ensure a clean and traceable workflow.

---

## 1. Summary

**Describe the purpose of this Pull Request.**  
What problem does it solve? What feature does it add? Why is it needed?

> Example:  
> This PR fixes the issue where the integration module fails to evaluate trigonometric and exponential functions using non‑`x` variables.

---

## 2. Related Issue / Ticket

Link the issue or ticket this PR addresses.

- Closes: #ISSUE_NUMBER  
- Related: #ISSUE_NUMBER

---

## 3. Branch Information

- **Source branch:**  
  `feature/...`  
  `bug/...`  
  `fix/...`  

- **Target branch:**  
  `dev` → for development  
  `qa` → for QA validation  
  `main` → for production releases

> PRs to `main` must come from `qa`.

---

## 4. Type of Change

Select all that apply:

- [ ] 🆕 Feature  
- [ ] 🐞 Bug fix  
- [ ] 🔧 Refactor  
- [ ] 📝 Documentation  
- [ ] 🎨 UI/UX adjustment  
- [ ] ⚙️ Build / Makefile / CI  
- [ ] 🔒 Hotfix  
- [ ] Other (specify):

---

## 5. Description of Changes

Provide a detailed explanation of what was changed.

- What modules were modified?  
- What functions/classes were added or updated?  
- Any architectural impact?  
- Any renderer/UIContract changes?

---

## 6. Testing Performed

Describe how you validated the changes.

### Unit Tests
- [ ] Added new tests  
- [ ] All tests pass locally  
  ```bash
  pytest -q
  ```

### Stress Tests
- [ ] Stress tests executed  
  ```bash
  pytest tests/stress
  ```

### Manual Testing
- [ ] Integration module validated  
- [ ] Renderer outputs validated  
- [ ] UIContract blocks validated  
- [ ] Edge cases tested (invalid inputs, special functions, etc.)

---

## 7. QA Validation (for PRs targeting `qa` or `main`)

- [ ] Functional tests passed  
- [ ] Regression tests passed  
- [ ] Performance acceptable  
- [ ] UI/UX consistent  
- [ ] No breaking changes  
- [ ] Meets acceptance criteria  

---

## 8. Documentation

- [ ] Updated docstrings  
- [ ] Updated Markdown documentation  
- [ ] Updated CHANGELOG (if applicable)

---

## 9. Checklist Before Merge

- [ ] Follows Conventional Commits  
- [ ] No debug prints  
- [ ] No commented-out code  
- [ ] No unrelated changes  
- [ ] Code is clean and readable  
- [ ] Branch is up-to-date with target branch  
- [ ] CI/CD checks pass  

---

## 10. Additional Notes

Add any extra context, screenshots, performance metrics, or considerations for reviewers.

---

# ✔ Ready for Review

---

