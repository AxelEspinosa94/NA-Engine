
---

# **NA‑Engine Makefile — Release & Formatting Workflow Documentation**

This document describes the structure, purpose, and behavior of the Makefile used in **NA‑Engine**. It covers both the **automated release tagging system** and the **Python formatting pipeline** powered by **Black**, **isort**, and **flake8**, including how the project’s `pyproject.toml` governs formatting rules.

---

## **1. Overview**

The NA‑Engine Makefile provides two major capabilities:

1. **Release Automation**  
   Automated semantic version tagging for PATCH and MINOR releases.

2. **Code Quality & Formatting Pipeline**  
   A unified formatting workflow using:
   - **Black** for deterministic code formatting  
   - **isort** for import ordering  
   - **flake8** for linting and static analysis  

The Makefile is designed to work consistently across Windows and Unix-like systems.

---

## **2. Cross‑Platform Python Resolution**

To ensure compatibility across environments, the Makefile detects the operating system and assigns the correct Python and pip executables:

- **Windows:**  
  `python.exe`, `pip.exe`

- **Unix / WSL:**  
  `python3`, `pip3`

This guarantees that formatting and release commands behave identically regardless of platform.

---

## **3. Release Automation**

The Makefile extracts the latest Git tag (e.g., `v0.1.1`) and parses it into:

- `MAJOR`
- `MINOR`
- `PATCH`

It then computes the next version depending on the release target.

### **3.1 Version Parsing Logic**

- Removes the leading `v`
- Splits the version into numeric components
- Uses shell arithmetic to compute:
  - `NEXT_PATCH`
  - `NEXT_MINOR`

### **3.2 Release Targets**

#### **release-patch**
Creates a new PATCH release:

- Increments the PATCH number  
- Creates an annotated tag  
- Pushes the tag to the remote  

#### **release-minor**
Creates a new MINOR release:

- Increments the MINOR number  
- Resets PATCH to `0`  
- Creates and pushes the new tag  

#### **release-patch-dry**
Outputs the actions that *would* be taken, without modifying the repository.

---

## **4. Code Formatting Pipeline**

NA‑Engine enforces consistent formatting using three tools:

### **Black — Code Formatter**
Black applies a strict, deterministic formatting style.  
It is **idempotent**, meaning once code is formatted, repeated runs produce no changes.

### **isort — Import Sorter**
isort organizes imports into logical sections and alphabetical order.  
In NA‑Engine, isort is configured to use the **Black profile**, ensuring both tools agree on formatting rules.

### **flake8 — Linter**
flake8 performs static analysis, detecting:

- unused imports  
- style violations  
- potential errors  

---

## **5. Formatting Targets**

### **format**
Applies formatting to the main project directories:

```
core/
strategies/
app/
tests/
```

This target runs:

1. `black` — formats code  
2. `isort` — sorts imports  

### **check-format**
Runs both tools in **verification mode**:

- `black --check`  
- `isort --check-only`  

If any file is not properly formatted, this target fails.  
This is ideal for CI/CD pipelines.

### **lint**
Runs `flake8` across the repository to detect style issues and unused imports.

---

## **6. Role of `pyproject.toml` in Formatting**

The formatting tools rely on a shared configuration stored in `pyproject.toml`.  
This file ensures **consistent behavior** between Black and isort.

### **6.1 Black Configuration**
Defines:

- line length  
- target Python version  
- excluded directories and legacy files  

Example exclusions include:

- documentation  
- notebooks  
- config files  
- legacy modules  
- non‑Python assets  

This prevents Black from attempting to parse or format files that should not be touched.

### **6.2 isort Configuration**
Defines:

- `profile = "black"` → ensures compatibility with Black  
- line length  
- first‑party modules (`core`, `strategies`, `app`)  

This prevents import‑ordering conflicts between Black and isort.

### **6.3 Why `pyproject.toml` Matters**
Without a shared configuration:

- Black and isort may disagree on formatting  
- `make format` and `make check-format` can enter infinite loops  
- imports may be repeatedly “fixed” and then flagged again  

The `pyproject.toml` ensures both tools operate with the same rules, stabilizing the formatting pipeline.

---

## **7. Recommended Developer Workflow**

1. **Before committing:**  
   Run `make format` to apply formatting.

2. **Before opening a pull request:**  
   Run `make check-format` to ensure the repo is clean.

3. **During development:**  
   Run `make lint` to catch unused imports or style issues.

4. **When publishing a new version:**  
   Use `make release-patch` or `make release-minor`.

---

## **8. Summary**

The NA‑Engine Makefile provides a robust workflow for:

- cross‑platform Python execution  
- automated semantic versioning  
- deterministic code formatting  
- import normalization  
- static linting  
- CI‑friendly formatting checks  

The integration with `pyproject.toml` ensures that Black and isort operate in harmony, keeping the codebase clean, stable, and contributor‑friendly.

---
