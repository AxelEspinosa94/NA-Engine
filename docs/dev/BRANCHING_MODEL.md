
---

# NA‑Engine — Branching Model

This document defines the branching strategy used in NA‑Engine.  
It ensures clarity, stability, and consistency across the entire development lifecycle, following a DevOps‑oriented workflow.

---

# 1. Overview

NA‑Engine uses a **three‑environment branching model**:

```
dev → qa → main
```

Each branch represents a different stage of stability and validation:

- **dev** — Development and integration
- **qa** — Quality assurance and validation
- **main** — Production‑ready code

Feature and bug branches feed into this pipeline.

---

# 2. Branch Roles

## 2.1 `dev` — Development Environment
The integration branch where active development occurs.

### Purpose
- Integrate feature branches
- Integrate bug fixes
- Run unit tests and stress tests
- Validate architecture and module consistency

### Rules
- No direct commits (only merges via Pull Requests)
- All work must come from:
  - `feature/*`
  - `bug/*`
  - `fix/*`

---

## 2.2 `qa` — Quality Assurance Environment
The validation branch where code is tested before production.

### Purpose
- Functional testing
- Regression testing
- Performance validation
- UI/UX consistency checks
- Renderer and output validation

### Rules
- Only receives code from `dev`
- Must pass all QA criteria before promotion to `main`
- No direct commits

---

## 2.3 `main` — Production Environment
The stable branch representing the production state of NA‑Engine.

### Purpose
- Holds production‑ready code
- Stores release tags (e.g., `v0.1.6`)
- Used for deployment and distribution
- Source of truth for public releases

### Rules
- **Protected branch**
- No direct pushes
- Only receives Pull Requests from `qa`
- All releases must be tagged from `main`

---

# 3. Supporting Branches

## 3.1 `feature/*`
Used for new features.

Examples:
```
feature/clenshaw-curtis
feature/adaptive-quadrature
feature/monte-carlo
```

Rules:
- Must branch off `dev`
- Must merge back into `dev` via Pull Request

---

## 3.2 `bug/*`
Used for bug fixes.

Examples:
```
bug/integration/functions_unrecognized
bug/renderer/latex-blocks
```

Rules:
- Must branch off `dev`
- Must merge back into `dev` via Pull Request

---

## 3.3 `fix/*`
Used for small fixes or refactors.

Examples:
```
fix/makefile-crossplatform
fix/ui-header-spacing
```

Rules:
- Must branch off `dev`
- Must merge back into `dev` via Pull Request

---

# 4. Promotion Workflow

## 4.1 `feature/bug/fix` → `dev`
- Code review required
- Unit tests must pass
- Stress tests must pass
- No direct commits to `dev`

---

## 4.2 `dev` → `qa`
- Functional validation
- Regression testing
- Performance testing
- UI/UX validation
- Renderer consistency checks

---

## 4.3 `qa` → `main`
- All QA criteria must pass
- Release notes prepared
- CHANGELOG updated
- Version bump confirmed
- Merge via Pull Request (Squash & Merge)
- Tag created from `main`

---

# 5. Branch Protection Rules

## `main`
- Require Pull Requests
- Block direct pushes
- Require status checks
- Require branch to be up‑to‑date before merging
- Require conversation resolution
- (Optional) Require signed commits

## `qa`
- Block direct pushes
- Require Pull Requests from `dev`

## `dev`
- Block direct pushes
- Require Pull Requests from feature/bug/fix branches

---

# 6. Release Flow

```
feature/* → dev → qa → main → tag → release
```

Tags follow semantic versioning:

```
vMAJOR.MINOR.PATCH
```

Examples:
```
v0.1.6
v0.2.0
v1.0.0
```

---

# 7. Summary

This branching model ensures:

- Clean separation of environments  
- Predictable release cycles  
- Stable production code  
- Clear workflow for features and bug fixes  
- Full DevOps compatibility  

NA‑Engine maintains a professional, scalable, and maintainable development pipeline.

```

---

