
---

# **VERSIONING**  
### *Semantic Versioning Guidelines for NA‑Engine*

---

## **1. Purpose**

This document defines the versioning rules used in NA‑Engine.  
The project follows a **pre‑1.0 semantic versioning model**, where the API is still evolving and breaking changes are allowed without requiring a major version bump.

The goal is to maintain consistency, clarity, and predictability across development stages.

---

## **2. Version Format**

NA‑Engine uses the following version format:

```
0.MINOR.PATCH
```

Where:

- **MINOR** — increases when new features, modules, or capabilities are added  
- **PATCH** — increases when fixes, refactors, documentation updates, or UI improvements are made  

Because the project is still in the `0.x.x` phase:

> **Breaking changes are allowed at any time without requiring a major version bump.**

---

## **3. General Rules**

### **3.1 MINOR Version Rules (`0.X.0`)**

Increase the **MINOR** version when:

- A new module is added (e.g., ODE, Integration, Nonlinear Systems)
- A new numerical method is introduced (e.g., RK4, Simpson Composite)
- A new UI component or feature is added
- A new subsystem is implemented (e.g., Documentation Module)
- A development Stage is completed (Stage 4 → Stage 5)

Examples:

```
0.1.0 → 0.2.0
0.2.0 → 0.3.0
```

---

### **3.2 PATCH Version Rules (`0.X.Y`)**

Increase the **PATCH** version when:

- Bugs are fixed
- UI is improved
- Code is refactored without adding new features
- Documentation is updated
- Internal behavior is improved but not expanded
- Folder structure is reorganized without adding new capabilities

Examples:

```
0.1.0 → 0.1.1
0.1.1 → 0.1.2
```

---

## **4. Stage‑Based Versioning**

NA‑Engine is developed in structured stages:

- **Stage 1** — Architecture  
- **Stage 2** — Numerical Modules  
- **Stage 3** — UI  
- **Stage 4** — Documentation  
- **Stage 5** — Advanced Integration / Polish  
- **Stage 6+** — Future expansions  

The rule is:

> **Each completed Stage increments the MINOR version.**

Example progression:

```
Stage 4 → v0.1.0
Stage 5 → v0.2.0
Stage 6 → v0.3.0
```

Fixes between stages increment PATCH:

```
v0.1.0 → v0.1.1 → v0.1.2
```

---

## **5. Tagging Rules**

### **5.1 When to Create a Tag**

Create a tag when:

- A Stage is completed  
- A stable feature set is reached  
- A release is ready for public or internal use  

### **5.2 Tag Format**

Tags use the format:

```
v0.MINOR.PATCH
```

Example:

```
v0.1.0
v0.1.1
v0.2.0
```

### **5.3 Tagging Commands**

```
git add .
git commit -m "Commit message"
git push origin <branch>
git tag -a v0.1.0 -m "NA-Engine v0.1.0 — Documentation Module"
git push origin v0.1.0
```

---

## **6. When NA‑Engine Reaches 1.0.0**

The project will move to:

```
1.0.0
```

when:

- All core numerical modules are complete  
- The UI is stable  
- The documentation system is fully integrated  
- The API is consistent and ready for external use  

After 1.0.0:

- **MAJOR** → breaking changes  
- **MINOR** → new features  
- **PATCH** → fixes  

---

## **7. Summary**

- NA‑Engine uses **0.MINOR.PATCH** until stable  
- **MINOR** = new features or completed Stages  
- **PATCH** = fixes, refactors, documentation  
- Breaking changes are allowed in `0.x.x`  
- Tags follow the format `v0.x.x`  
- Each Stage completion increments MINOR  

This versioning strategy keeps NA‑Engine clean, predictable, and easy to maintain as it grows.

## **8. Useful commands**

To know what is the current tag
```bash
git describe --tags --abbrev=0
```

To know if there are commits after a tag
```bash
git log v0.1.1..HEAD --oneline
```

Just in case, but the tagging thing will be performed by a `make release` procedure

```batch
make release-patch 
make release-minor
```
---

