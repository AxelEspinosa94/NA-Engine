
---

# **Deferred CI Enhancements — Stage 6 & Stage 7 Roadmap**

This document outlines the CI/CD features intentionally deferred for future development stages of **NA‑Engine**. These enhancements are not required for the current development cycle but will become relevant as the project grows, gains contributors, and moves toward broader release automation.

---

## **Overview**

During the initial CI design, several advanced features were identified as valuable but not immediately necessary. These items have been categorized into:

- **Stage 6 Enhancements** — Features that improve release automation, multi-version compatibility, debugging capabilities, and artifact management.
- **Stage 7 Enhancements** — Features related to contributor workflow enforcement and repository hygiene.

This document serves as a roadmap for implementing these deferred capabilities once NA‑Engine reaches the appropriate maturity level.

---

# **Stage 6 — Advanced CI/CD Enhancements**

Stage 6 focuses on expanding NA‑Engine’s CI pipeline beyond basic testing and formatting. These features enhance reliability, compatibility, and automation but are not essential while the project remains Python‑3.12‑exclusive and primarily single‑contributor.

---

## **1. Python Version Matrix (3.10, 3.11, 3.12)**

### **Description**
Introduce multi-version testing across Python 3.10, 3.11, and 3.12 using a GitHub Actions matrix.

### **Purpose**
- Ensure NA‑Engine is compatible with multiple Python versions.
- Detect version-specific issues in numerical libraries (NumPy, SciPy, Dash).
- Prepare the project for broader distribution (PyPI, conda).

### **Reason for Deferral**
The project currently targets **Python 3.12 exclusively**.  
Multi-version support will be introduced once Stage 6 begins and backward compatibility becomes a priority.

---

## **2. CI Artifacts (Logs, Coverage Reports, HTML Reports)**

### **Description**
Upload test artifacts (coverage reports, stress test logs, HTML test reports) as downloadable files in GitHub Actions.

### **Purpose**
- Improve debugging for complex failures.
- Provide QA visibility into stress test output.
- Enable regression analysis and historical test tracking.

### **Reason for Deferral**
Debugging needs are minimal at this stage.  
Artifacts become more valuable once the project grows and more contributors join.

---

## **3. Automatic Build + Release (GitHub Releases)**

### **Description**
Automatically generate GitHub Releases when a tag is created, including:

- version number  
- changelog  
- optional build artifacts  

### **Purpose**
- Fully automate the release pipeline.
- Ensure consistent release metadata.
- Reduce manual overhead.

### **Reason for Deferral**
Manual releases are sufficient for now.  
Automation will be introduced once NA‑Engine reaches a stable public distribution phase.

---

## **4. Automatic Tagging on Merge to `main`**

### **Description**
CI automatically creates a PATCH or MINOR tag when a PR is merged into `main`.

### **Purpose**
- Enforce semantic versioning.
- Guarantee every merge produces a versioned release.
- Remove manual tagging steps.

### **Reason for Deferral**
Tagging logic requires:
- PR labels (`release:patch`, `release:minor`)  
- or conventional commit parsing  
- or file-based heuristics  

This workflow becomes relevant once more contributors participate and releases become more frequent.

---

# **Stage 7 — Contributor Workflow & Repository Hygiene**

Stage 7 focuses on enforcing contributor standards and repository cleanliness once NA‑Engine becomes a multi-developer project.

---

## **1. Pre‑commit Hook Enforcement**

### **Description**
Require contributors to run pre‑commit hooks locally before pushing code.  
Hooks typically include:

- Black formatting  
- isort import sorting  
- flake8 linting  
- trailing whitespace removal  
- file permission normalization  

### **Purpose**
- Prevent CI failures caused by formatting issues.
- Maintain a clean and consistent codebase.
- Reduce noise in pull requests.

### **Reason for Deferral**
You are currently the sole contributor.  
Pre‑commit enforcement becomes valuable once external contributors join.

---

# **Summary Table**

| Feature | Stage | Purpose | Reason Deferred |
|--------|-------|---------|-----------------|
| Python version matrix | 6 | Multi-version compatibility | Project is 3.12-only |
| CI artifacts | 6 | Debugging & QA visibility | Not needed yet |
| Automatic GitHub Release | 6 | Full release automation | Manual releases are fine |
| Automatic tagging | 6 | Semantic versioning automation | Requires PR labels or commit rules |
| Pre‑commit enforcement | 7 | Contributor workflow hygiene | Single-contributor project |

---

# **Conclusion**

These deferred enhancements form the backbone of NA‑Engine’s future CI/CD evolution.  
Stage 6 will introduce automation, compatibility, and debugging improvements, while Stage 7 will enforce contributor standards and repository hygiene.

Once the project reaches the appropriate maturity level, each of these features can be integrated seamlessly into the existing CI pipeline.

---

