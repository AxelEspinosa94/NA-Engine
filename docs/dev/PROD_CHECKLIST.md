
---

# NA‑Engine — Production Checklist (MAIN)

This checklist defines all required steps before promoting code from the
`qa` environment into `main` (production).  
Production represents the stable, public, versioned state of NA‑Engine.

---

# 1. Branch Requirements

- [ ] PR source is `qa`
- [ ] PR target is `main`
- [ ] Branch is up-to-date with `main`
  ```bash
  git pull origin main
  ```
- [ ] No direct commits to `main`
- [ ] All changes in the PR are intended for the release

---

# 2. Final QA Validation

Confirm that QA has fully validated the release:

- [ ] Functional tests passed
- [ ] Regression tests passed
- [ ] Stress tests passed
- [ ] Performance acceptable
- [ ] UI/UX validated
- [ ] Renderer outputs correct blocks
- [ ] No breaking changes introduced
- [ ] All acceptance criteria met

---

# 3. Release Readiness

Validate that the release is complete and consistent:

- [ ] Version bump applied in the application header
- [ ] Version bump applied in metadata (if applicable)
- [ ] CHANGELOG updated and finalized
- [ ] Documentation updated
- [ ] Examples updated (if applicable)
- [ ] Release notes drafted

---

# 4. CI/CD Validation

- [ ] GitHub Actions pipeline passes for `main`
- [ ] No warnings or errors in logs
- [ ] PR follows PULL_REQUEST_TEMPLATE
- [ ] All checks green

---

# 5. Merge Requirements

- [ ] PR reviewed and approved (self-approval allowed if solo)
- [ ] Merge performed using **Squash & Merge**
- [ ] No merge conflicts
- [ ] Commit history clean and readable

---

# 6. Tagging the Release

After merging into `main`, create the release tag:

### Patch Release
```bash
make release-patch
```

### Minor Release
```bash
make release-minor
```

### Major Release
```bash
make release-major
```

Validate:

- [ ] Tag created successfully
- [ ] Tag pushed to GitHub
- [ ] Tag visible in GitHub Releases

---

# 7. Publishing the Release

- [ ] Create GitHub Release
- [ ] Attach release notes
- [ ] Link to CHANGELOG
- [ ] Mark release as stable
- [ ] Add screenshots or examples (optional)

---

# 8. Post‑Release Tasks

- [ ] Delete release branch:
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
- [ ] Update roadmap (if applicable)

---

# ✔ Production Stage Completed — Release Published

---
