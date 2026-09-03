
---

# **NA‑Engine Continuous Integration (CI) Overview**

This document describes the Continuous Integration (CI) workflow used in **NA‑Engine**, including branch rules, test tiers, formatting checks, linting, and automatic tagging. The CI pipeline is implemented using **GitHub Actions** and is defined in `tests.yml`.

---

## **1. CI Goals**

The CI system in NA‑Engine is designed to:

- Ensure code quality and formatting consistency.
- Validate all contributions through automated testing.
- Enforce branch‑based testing tiers (dev, qa, main).
- Support feature and fix branches tied to each environment.
- Automatically tag releases when merging into `main`.
- Provide fast feedback for developers and stable validation for release candidates.

---

# **2. Branch Strategy**

NA‑Engine uses a structured branch model inspired by PHOBOS:

### **Primary branches**
- `dev` — development environment  
- `qa` — quality assurance environment  
- `main` — production-ready environment  

### **Feature branches**
- `feature/dev/*`  
- `feature/qa/*`  
- `feature/main/*`  

### **Fix branches**
- `fix/dev/*`  
- `fix/qa/*`  
- `fix/main/*`  

### **CI triggers**
The CI pipeline runs on:

- pushes to any of the branches above  
- pull requests targeting any of the branches above  

This ensures that **every change**, whether experimental or production-bound, is validated before merging.

---

# **3. CI Jobs Overview**

The CI pipeline is composed of several jobs, each responsible for a specific validation stage.

---

## **3.1 Lint Job (flake8)**

Runs independently and early in the pipeline.

### **Purpose**
- Detect unused imports  
- Identify style violations  
- Catch potential logical issues  

### **Why separate?**
A dedicated lint job provides faster feedback and avoids mixing lint errors with formatting or test failures.

---

## **3.2 Formatting Check (Black + isort)**

Runs after linting and before any tests.

### **Purpose**
- Enforce deterministic formatting (Black)
- Enforce import ordering (isort)
- Prevent formatting issues from reaching test stages

### **Configuration**
Formatting rules are defined in `pyproject.toml`, ensuring:

- Black and isort share the same style profile  
- First‑party modules (`core`, `strategies`, `app`) are recognized  
- Legacy or non-Python files are excluded  

If formatting fails, CI stops immediately.

---

## **3.3 Test Tiers**

NA‑Engine uses three test tiers depending on the branch.

---

### **DEV Tier — Fast Tests (Linux only)**

Runs on:

- `dev`
- `feature/dev/*`
- `fix/dev/*`

### **Tests executed**
- Unit tests  
- Integration tests  

### **Purpose**
Fast feedback for active development.

---

### **QA Tier — Full Tests (Multiplatform + Stress)**

Runs on:

- `qa`
- `feature/qa/*`
- `fix/qa/*`

### **Tests executed**
- Unit tests  
- Integration tests  
- Stress tests  

### **Platforms**
- Ubuntu  
- Windows  
- macOS  

### **Purpose**
Cross-platform validation before promoting changes to `main`.

---

### **MAIN Tier — Final Validation**

Runs on:

- `main`
- `feature/main/*`
- `fix/main/*`

### **Tests executed**
- Full test suite (unit + integration + stress)

### **Purpose**
Final gate before release.

---

# **4. Automatic Tagging**

When a pull request is merged into `main`, the CI automatically creates a new version tag.

### **Tag type is determined by PR labels:**
- `release:minor` → MINOR version bump  
- Any other label → PATCH version bump  

### **Versioning rules**
If current version is `vX.Y.Z`:

- **PATCH:** → `vX.Y.(Z+1)`  
- **MINOR:** → `vX.(Y+1).0`  

### **Purpose**
- Enforce semantic versioning  
- Automate release preparation  
- Reduce manual tagging errors  

This system mirrors the PHOBOS workflow and keeps NA‑Engine’s release history clean and predictable.

---

# **5. Why Formatting and Linting Run Before Tests**

Running formatting and linting before tests ensures:

- CI fails fast on stylistic issues  
- Test logs remain focused on functional failures  
- Contributors receive clear feedback  
- The codebase remains consistent across environments  

This ordering is intentional and follows best practices for Python projects.

---

# **6. Future CI Enhancements (Stage 6 & 7)**

Some advanced CI features are intentionally deferred:

### **Stage 6**
- Python version matrix (3.10, 3.11, 3.12)  
- CI artifacts (coverage, logs, HTML reports)  
- Automatic GitHub Releases  
- Extended debugging support  

### **Stage 7**
- Pre‑commit hook enforcement  
- Contributor workflow automation  

These features will be added once NA‑Engine reaches broader distribution and multi‑contributor activity.

---

# **7. Summary**

The NA‑Engine CI pipeline provides:

- Deterministic formatting  
- Strict linting  
- Tiered testing based on branch type  
- Multiplatform validation for QA and MAIN  
- Automatic semantic version tagging  
- Full compatibility with the project’s branching strategy  

This ensures that every change is validated, consistent, and ready for promotion through the development pipeline.

---
