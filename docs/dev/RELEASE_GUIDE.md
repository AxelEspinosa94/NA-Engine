
---

# NA‑Engine — Release Guide

This document describes the complete release workflow for NA‑Engine, covering
branch promotion, versioning, tagging, changelog updates, and deployment.
It is designed to support a DevOps‑oriented pipeline using the
`dev → qa → main` branching model.

---

# 1. Overview

A release in NA‑Engine follows this sequence:

```
feature/bug/fix → dev → qa → main → tag → release
```

Each stage has strict criteria to ensure stability, reproducibility, and
professional release management.

---

# 2. Release Types

NA‑Engine follows **Semantic Versioning (SemVer)**:

```
MAJOR.MINOR.PATCH
```

### 2.1 Patch Release (`vX.Y.Z+1`)
Used for:
- Bug fixes
- Minor improvements
- Non-breaking changes

### 2.2 Minor Release (`vX.Y+1.0`)
Used for:
- New features
- Significant module updates
- Backwards-compatible enhancements

### 2.3 Major Release (`vX+1.0.0`)
Used for:
- Breaking changes
- Architectural changes
- Major redesigns

---

# 3. Pre‑Release Checklist

Before promoting code to QA:

- [ ] All feature/bug/fix branches merged into `dev`
- [ ] All unit tests pass
- [ ] Stress tests pass
- [ ] No debug prints or commented-out code
- [ ] Renderer outputs validated
- [ ] UIContract consistency verified
- [ ] Documentation updated
- [ ] CHANGELOG draft prepared

---

# 4. Promotion to QA

Promote `dev` → `qa` via Pull Request.

### QA Validation Checklist

- [ ] Functional tests pass
- [ ] Regression tests pass
- [ ] Performance acceptable
- [ ] UI/UX validated
- [ ] Numerical correctness validated
- [ ] No breaking changes introduced
- [ ] All acceptance criteria met

Once QA approves, the release is ready for production.

---

# 5. Preparing the Release Branch

Create a release branch from `qa`:

```bash
git checkout qa
git pull
git checkout -b release/vX.Y.Z
```

Update:

- [ ] Version number in the application header
- [ ] CHANGELOG.md (finalized)
- [ ] Documentation (if needed)

Push the branch:

```bash
git push origin release/vX.Y.Z
```

---

# 6. Promotion to Production (Main)

Create a Pull Request:

```
Base: main
Compare: release/vX.Y.Z
```

### Production Merge Requirements

- [ ] All QA checks passed
- [ ] CHANGELOG finalized
- [ ] Version bump confirmed
- [ ] Release notes prepared
- [ ] CI/CD checks passed
- [ ] PR reviewed and approved

Merge using **Squash & Merge**.

---

# 7. Tagging the Release

Once merged into `main`, create the tag using the Makefile.

### Patch Release

```bash
make release-patch
```

### Minor Release

```bash
make release-minor
```

This will:

- Create the annotated tag
- Push the tag to GitHub
- Update version metadata

Verify the tag:

```bash
git tag -l
```

---

# 8. Publishing the Release

After tagging:

- [ ] Create a GitHub Release
- [ ] Attach release notes
- [ ] Link to CHANGELOG
- [ ] Mark as stable

Optional:

- [ ] Add screenshots
- [ ] Add module examples
- [ ] Add performance benchmarks

---

# 9. Post‑Release Tasks

After the release is published:

- [ ] Delete the release branch:
  ```bash
  git push origin --delete release/vX.Y.Z
  ```

- [ ] Sync `dev` with `main`:
  ```bash
  git checkout dev
  git pull
  git merge main
  git push origin dev
  ```

- [ ] Close related issues and tickets
- [ ] Update roadmap if needed

---

# 10. Hotfix Workflow

If a critical issue is found in production:

1. Create a hotfix branch from `main`:
   ```bash
   git checkout main
   git checkout -b hotfix/<description>
   ```

2. Fix the issue and push the branch.

3. Create PR:
   ```
   Base: main
   Compare: hotfix/<description>
   ```

4. Merge and tag:
   ```bash
   make release-patch
   ```

5. Promote fix back to `qa` and `dev` to keep environments aligned.

---

# 11. Summary

The NA‑Engine release workflow ensures:

- Stable production releases  
- Predictable versioning  
- Full traceability  
- Clean branching model  
- Compatibility with CI/CD automation  

By following this guide, every release remains consistent, professional, and
aligned with the long‑term architecture of NA‑Engine.

---

