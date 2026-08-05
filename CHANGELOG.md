# Changelog

---

## NA-Engine v0.1.5 — Stage 5 Patch 2: Unified Output Renderer + Matrix LaTeX + Header Upgrade
**Release date:** 2026-08-04

### Added
- Unified output rendering system with multi-block support.
- Tooltip integration for all output blocks (scalar, vector, matrix, plots, tables, markdown).
- LaTeX rendering for:
  - Matrices (L, U, P)
  - Vectors (solution vectors)
  - Matrix groups (LU, QR)
- New `matrix_expression` block type for mathematical outputs. (Will substitute the original `matrix` block type)
- Dynamic version display in the header using Git tags.
- New header design with gradient typography and theme-aware styling.

### Improved
- Output blocks now follow consistent styling per module (Interpolation, Integration, Linear Algebra, etc.).
- Enhanced KEY_DISPATCH to support multi-output detection (value, expression, table, plot, matrix groups).
- Renderer now produces structured multi-block payloads for the UIContract.
- Matrix group renderer upgraded to include raw values + LaTeX expressions.
- Cleaned and standardized result-area layout for readability and coherence.
- Improved dark/light mode compatibility across output components.

### Notes
This patch completes the foundational work for Stage 5’s rendering architecture.  
Upcoming patches will focus on:
- Advanced ODE/BVP visualization
- Export tools (PDF, LaTeX, CSV)
- Responsive layout improvements
- Full i18n migration (English/Spanish)

---

## NA-Engine v0.1.4 — Stage 5 Patch 1: UI/UX Foundation + Tooltip System
**Release date:** 2026-07-28

### Added
- Global UI/UX foundation for all modules.
- Unified styling for:
  - Numeric inputs
  - Text inputs
  - Dropdowns
  - RadioItems
  - Buttons
  - Error states
  - Hover/disabled states
- Complete tooltip system with:
  - Tooltip icon component
  - Tooltip input wrapper
  - Light/dark mode support
  - Hover/click interactions
- Full tooltip coverage for:
  - Nonlinear Equations
  - Numerical Derivatives
  - Numerical Integration
  - Interpolation
  - Linear Algebra

### Improved
- Standardized layout containers across modules.
- Cleaned legacy CSS and removed inconsistent styles.
- Improved readability and consistency of UI components.
- Prepared structure for future i18n (English migration not yet active).

### Notes
This patch establishes the visual and structural foundation for Stage 5.  
Upcoming patches will focus on new numerical methods, advanced ODE/BVP features, responsiveness, export tools, and i18n.

---

## NA-Engine v0.1.3 — About Section

### Added
- About section

### Improved
- Consistent styling across modules
- Better separation of UI concerns
- Cleaner callback structure

### Notes
This version is a patch before improvements to take place in Stage 5.

---

## NA-Engine v0.1.0 — MVP

### Added
- New dynamic documentation module
- Markdown rendering with MathJax support
- Dark/light theme support for theoretical content
- New folder structure under docs/theory/<module>/<method>.md
- UI integration with module/method selectors
- Architecture documentation for the documentation module

### Improved
- Consistent styling across modules
- Better separation of UI concerns
- Cleaner callback structure

### Notes
This version completes Stage 4 of NA-Engine.

---