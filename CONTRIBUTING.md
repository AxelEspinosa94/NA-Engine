
---

# 📘 **CONTRIBUTING.md — NA‑Engine (Professional Edition, English)**

# Contributing to NA‑Engine

Thank you for your interest in contributing to **NA‑Engine**, a modular numerical analysis engine with a clean architecture, consistent UI/UX, and an advanced rendering system.  
This document outlines the workflow, standards, and recommended practices for contributing to the project.

---

## 🧱 1. Environment Setup

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### WSL / Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the application
```bash
python app.py
```

---

## 🌿 2. Branch Workflow (Simplified Git Flow)

NA‑Engine uses a branch‑based workflow to maintain stability, clarity, and a clean project history.

### Main branches
- **main** → Stable code and released versions.
- **develop** → Integration of new features before release.

### Working branches
- **feature/** → New features.
- **fix/** → Specific fixes.
- **hotfix/** → Urgent patches for `main`.
- **release/** → Version preparation (tags, changelog, documentation).

Examples:
```
feature/stage5-renderer
feature/output-tooltips
fix/makefile-crossplatform
release/v0.1.5
```

---

## ✏️ 3. Commit Standards (Conventional Commits)

We use **Conventional Commits** to maintain a readable and structured commit history.

### Allowed types
- `feat:` → New feature
- `fix:` → Bug fix
- `refactor:` → Internal change without altering functionality
- `docs:` → Documentation
- `style:` → Formatting or style changes
- `test:` → Tests
- `build:` → Makefile, dependencies, CI/CD
- `chore:` → General maintenance

### Examples
```
feat(renderer): add matrix group LaTeX support
fix(contract): correct multi-block dispatch for matrix outputs
style(ui): unify header gradient and spacing
build(makefile): add cross-platform arithmetic for Windows
```

---

## 🛠️ 4. Working on a New Feature

1. Create a branch from `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```

2. Commit using Conventional Commits.

3. Keep the branch focused on a single objective.

4. Update documentation if needed.

5. Ensure the application runs without errors.

---

## 🔀 5. How to Push Changes and Create a Merge Request to `main` (Important)

Even if you are the only contributor, following this workflow keeps the project clean and stable.

### Step 1 — Ensure your branch is up to date
```bash
git checkout feature/your-feature
git pull origin develop
```

### Step 2 — Merge recent changes from develop
```bash
git merge develop
```

Resolve conflicts if necessary.

### Step 3 — Push your branch
```bash
git push origin feature/your-feature
```

### Step 4 — Create a Merge Request (Pull Request)

On GitHub:

- **Base branch:** `main`
- **Compare branch:** `feature/your-feature`
- Provide a clear title (e.g., “Stage 5: Unified Output Renderer”)
- Provide a detailed description:
  - What was added
  - What was improved
  - Which modules are affected
  - Screenshots if applicable

### Step 5 — Review

Even if you are the only contributor, review your own PR as if you were someone else:

- Is the code clear?
- Any duplication?
- Does the renderer remain consistent?
- Does the UI maintain coherence?
- Does the Makefile still work cross‑platform?

### Step 6 — Merge into main

When everything is ready:

- Use **Squash and merge** (recommended)
- This keeps the history clean and readable.

### Step 7 — Create the release

Use the Makefile:

```bash
make release-patch
```

or

```bash
make release-minor
```

---

## 📦 6. Release Preparation

1. Update `CHANGELOG.md`
2. Create a release branch:
   ```bash
   git checkout -b release/vX.Y.Z
   ```
3. Update documentation if needed
4. Merge into `main`
5. Create tag using the Makefile
6. Push the tag

---

## 🧪 7. Testing

Run tests:
```bash
pytest -q
```

Stress tests:
```bash
pytest tests/stress
```

---

## 📚 8. Code Style Guidelines

- Python: snake_case for functions, PascalCase for classes.
- Keep modules small and focused.
- Avoid functions longer than ~40 lines when possible.
- Document public functions.
- Maintain consistency across renderers and UIContract.
- Keep output blocks visually coherent across modules.

---

## 🤝 9. General Contribution Rules

- Maintain compatibility with light/dark themes.
- Avoid introducing unnecessary dependencies.
- Do not mix multiple features in a single PR.
- Maintain visual consistency across modules.
- Keep KEY_DISPATCH and renderer aligned.
- Ensure Makefile works on both Windows and WSL.

---

## 🏁 10. Project Philosophy

NA‑Engine aims to be:

- Modular  
- Extensible  
- Consistent  
- Elegant  
- Maintainable  
- Professional  

Every contribution should respect these principles.

---
