
---

# **NA‑Engine — Documentation Module Architecture**  
### *Module Overview & Integration Guide*

---

## **1. Purpose**

The Documentation Module provides a unified interface for rendering theoretical content stored in the repository under `docs/theory`. It allows users to select a module and a method, and dynamically loads the corresponding Markdown file into the UI. The system supports mathematical notation via MathJax and ensures consistent styling across light and dark themes.

This module is designed to be:

- **Extensible** — new documentation files can be added without modifying the code  
- **Consistent** — unified UI/UX across all NA‑Engine modules  
- **Dynamic** — content is loaded on demand based on user selection  
- **Math‑aware** — supports LaTeX expressions inside Markdown  

---

## **2. Directory Structure**

The documentation files follow a strict folder hierarchy:

```
docs/
 └── theory/
      ├── derivatives/
      │     ├── forward.md
      │     ├── backward.md
      │     └── ...
      ├── integration/
      │     ├── trapezoid_simple.md
      │     └── ...
      ├── ode/
      │     ├── euler.md
      │     ├── rk2.md
      │     ├── rk4.md
      │     └── ...
      └── nonlinear/
            ├── bisection.md
            ├── newton.md
            └── ...
```

Each Markdown file corresponds to a method supported by NA‑Engine.

---

## **3. UI Architecture**

The documentation module is composed of three main UI elements:

### **3.1 Module Selector**
A dropdown listing all supported NA‑Engine modules:

- Derivatives  
- Integration  
- Linear Algebra  
- Nonlinear Equations  
- ODE  

### **3.2 Method Selector**
Populated dynamically based on the selected module.  
Each module exposes its own list of methods.

### **3.3 Documentation Display Area**
A dedicated section (`docs-result-area`) where the Markdown content is rendered.

This area supports:

- headings  
- lists  
- tables  
- code blocks  
- MathJax equations  
- custom CSS themes  

---

## **4. Callback Flow**

The module uses two main callbacks:

### **4.1 Method Loading Callback**
Triggered when the user selects a module.

Responsibilities:

- reveal the method dropdown  
- populate method options  
- prepare the UI for documentation loading  

### **4.2 Documentation Rendering Callback**
Triggered when the user clicks **“Show Documentation”**.

Responsibilities:

1. Build the file path based on module + method  
2. Load the Markdown file  
3. Render it using `dcc.Markdown`  
4. Enable MathJax rendering  
5. Apply the `markdown-doc` CSS theme  

This callback ensures that documentation is loaded dynamically without requiring page reloads.

---

## **5. MathJax Integration**

MathJax is activated globally through a custom `app.index_string` in `app.py`.

This enables rendering of:

- inline math: `\( ... \)`  
- display math: `$$ ... $$`  
- fenced math blocks: ```math  

MathJax automatically processes new content injected into the DOM by Dash.

---

## **6. Markdown Rendering**

The module uses Dash’s built‑in Markdown renderer:

```python
dcc.Markdown(content, mathjax=True, className="markdown-doc")
```

Key features:

- supports GitHub‑style Markdown  
- supports fenced code blocks  
- supports tables  
- supports embedded LaTeX  
- integrates with custom CSS themes  

No preprocessing or HTML injection is required.

---

## **7. Styling & Themes**

The documentation module uses the `.markdown-doc` class for styling.

### **Light Theme**
Applied by default.  
Provides:

- clean spacing  
- readable typography  
- consistent layout with NA‑Engine  

### **Dark Theme**
Activated when `#app-container.dark` is present.  
Uses custom CSS variables:

```css
--color-bg
--color-bg-alt
--color-text
--color-accent
--color-accent-dark
--color-border
```

The dark theme ensures:

- proper contrast  
- readable math expressions  
- consistent code block styling  
- GitHub‑style dark documentation aesthetics  

---

## **8. Extending the Module**

To add new documentation:

1. Create a new `.md` file under the appropriate folder  
2. Ensure the filename matches the method name  
3. Add the method to the module’s method list in the callback  
4. No further changes are required  

The module automatically detects and loads the new file.

---

## **9. Error Handling**

If a documentation file is missing:

- the callback returns a styled error message  
- the UI remains responsive  
- no crash occurs  

This ensures robustness during development and CI/CD.

---

## **10. CI/CD Integration**

The documentation module is fully compatible with GitHub Actions.

Recommended checks:

- ensure all `.md` files exist  
- validate folder structure  
- ensure no broken paths  
- ensure MathJax loads correctly  

Documentation rendering is not part of stress tests, but Markdown files can be linted.

---

## **11. Summary**

The Documentation Module provides:

- a unified interface for theoretical content  
- dynamic loading of Markdown files  
- full MathJax support  
- consistent styling across themes  
- easy extensibility  
- robust architecture aligned with NA‑Engine’s modular design  

This module completes Stage 4 by providing a polished, professional, and scalable documentation system.

---

