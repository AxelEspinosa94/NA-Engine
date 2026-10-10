
---

# NA‑Engine — Environments

This document describes the environments used in NA‑Engine and how they map
to branches, workflows, and release stages.  
It is designed to support a DevOps‑oriented lifecycle with clear separation
of responsibilities and stability levels.

---

## 1. Overview

NA‑Engine uses three logical environments:

- **Development (DEV)**
- **Quality Assurance (QA)**
- **Production (PROD)**

These environments are mapped directly to Git branches:

- **DEV → `dev`**
- **QA → `qa`**
- **PROD → `main`**

---

## 2. Development Environment (DEV)

### Branch
- `dev`

### Purpose
The Development environment is where active work happens:

- Feature implementation
- Bug fixing
- Refactoring
- Architectural changes
- Integration of multiple feature/bug/fix branches

### Typical Activities
- Creating `feature/*`, `bug/*`, `fix/*` branches
- Running unit tests and stress tests
- Validating integration between modules (e.g., integration, interpolation, linear algebra)
- Adjusting renderers and UIContract behavior

### Stability Level
- **Low to Medium**
- Code may be incomplete or experimental
- Breaking changes are allowed as long as they are stabilized before promotion to QA

### Rules
- No direct commits to `dev`
- All changes must come from:
  - `feature/*`
  - `bug/*`
  - `fix/*`
- Merges must be done via Pull Requests

---

## 3. Quality Assurance Environment (QA)

### Branch
- `qa`

### Purpose
The QA environment is used to validate that the code is ready for production:

- Functional testing
- Regression testing
- Performance testing
- UI/UX validation
- Renderer and output consistency checks

### Typical Activities
- Deploying the current `dev` state into `qa`
- Running test suites against realistic scenarios
- Validating numerical correctness (integration, interpolation, etc.)
- Checking visual consistency across modules
- Verifying that new features do not break existing ones

### Stability Level
- **Medium to High**
- Code should be feature‑complete for the upcoming release
- No experimental changes
- Only bug fixes and polish are allowed

### Rules
- Only receives changes from `dev`
- No direct commits to `qa`
- Merges must be done via Pull Requests from `dev`
- All QA criteria must be met before promotion to `main`

---

## 4. Production Environment (PROD)

### Branch
- `main`

### Purpose
The Production environment represents the stable, released state of NA‑Engine:

- Public releases
- Tagged versions
- Reference for users and external integrations
- Source of truth for deployment

### Typical Activities
- Creating release tags (e.g., `v0.1.6`)
- Running smoke tests
- Publishing release notes
- Updating documentation and CHANGELOG
- Serving as the base for hotfixes if needed

### Stability Level
- **Very High**
- Only production‑ready code
- No experimental features
- No breaking changes without a planned release

### Rules
- **Protected branch**
- No direct pushes
- Only receives Pull Requests from `qa`
- All tests and checks must pass before merging
- All releases must be tagged from `main`

---

## 5. Environment Promotion Flow

The promotion flow between environments is:

```text
feature/bug/fix → dev → qa → main
```

### 5.1 DEV Promotion Criteria (`feature/bug/fix` → `dev`)
- Code compiles and runs locally
- Unit tests pass
- Stress tests pass (if applicable)
- Code reviewed via Pull Request
- No unrelated changes included

### 5.2 QA Promotion Criteria (`dev` → `qa`)
- Functional tests pass
- Regression tests pass
- Performance within acceptable limits
- UI/UX validated
- Renderer and output blocks consistent

### 5.3 PROD Promotion Criteria (`qa` → `main`)
- All QA criteria met
- CHANGELOG updated
- Version bump confirmed
- Release notes prepared
- Merge via Pull Request (Squash & Merge)
- Tag created from `main`

---

## 6. Hotfixes

In case of critical issues in production:

- Create a branch from `main`:
  ```bash
  git checkout main
  git checkout -b hotfix/<description>
  ```
- Fix the issue
- Merge into `qa` and `dev` to keep environments in sync
- Promote back to `main` via Pull Request

---

## 7. Summary

The environment model for NA‑Engine ensures:

- Clear separation between development, testing, and production
- Predictable promotion flow
- Stable releases
- Full compatibility with CI/CD and DevOps practices

By strictly respecting the roles of `dev`, `qa`, and `main`, NA‑Engine maintains a professional and scalable development lifecycle.


---
