
---

# 📘 **NA‑Engine — Numerical Analysis Engine (Python 3.12, MIT License)**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-Dash-0099ff?logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
  <img src="https://img.shields.io/badge/Tests-pytest-blueviolet" />
  <img src="https://img.shields.io/badge/Domain-Numerical%20Analysis-orange" />
  <img src="https://img.shields.io/github/actions/workflow/status/AxelEspinosa94/NA-Engine/tests.yml?branch=main&label=CI%20Tests&color=brightgreen&style=flat" />
</p>

---

# 🧩 Overview

**NA‑Engine** is a modular, extensible, and interactive engine for solving **Numerical Methods**, **Numerical Analysis**, and **Differential Equations** problems.  
Built with **Python 3.12** and powered by **Dash**, it provides automated computations, mathematical rendering, plotting, and structured outputs for academic, scientific, and engineering use.

Its architecture is fully layered, separating:

- Construction  
- Validation  
- Execution  
- Rendering  
- UI Contract  
- Dash UI  

This makes the engine highly testable, maintainable, and easy to extend.

---

# 🚀 Features

### 🔧 Core Capabilities
- Interactive Dash web application  
- Hybrid input modes:
  - Editable tables  
  - Function‑generated nodes  
  - File uploads (CSV, TXT, Excel, JSON)

### 📐 Numerical Methods
- **Interpolation**: Newton, Lagrange, Cubic Splines, Hermite  
- **Numerical Integration**: Simpson, Trapezoidal  
- **Non‑linear Systems**: Fixed Point, Bisection, Secant, Newton–Raphson, False Position  
- **Differential Equations**:
  - Euler  
  - Heun  
  - RK2, RK4  
  - RKF45  
  - Systems of ODEs  
  - Shooting & Finite Differences (BVP)  
  - Adams–Bashforth & Adams–Moulton  
- **Matrix Methods**: LU, Cholesky, Gauss, Inverse, Determinant  
- **Numerical Derivatives**: forward, backward, central, higher‑order  

### 🧱 Architecture
- Modular OOP design  
- Clean separation between UI, callbacks, and computation logic  
- Extensible method catalog (JSON‑based)  
- Typed payload rendering (scalar, vector, matrix, plot, table, markdown)

### 🧪 Hybrid Testing Environment
- **Local unit tests** (pytest) for numerical algorithms  
- **Server‑side integration tests** via GitHub Actions  
- **Local UI interaction tests** using `dash.testing`  

> Los entornos de pruebas son híbridos:  
> - Los **unit tests** se ejecutan localmente sobre los métodos numéricos.  
> - Los **integration tests** corren en GitHub Actions para validar el pipeline completo.  
> - Las pruebas de UI se ejecutan localmente con `dash.testing` durante el MVP.

---

# 📁 Repository Structure

```
NA-Engine/
│
├── app/
│   ├── app.py
│   ├── layout/
│   ├── callbacks/
│   ├── components/
│   └── assets/
│
├── core/
│   ├── base_method.py
│   ├── contract.py
│   ├── renderer.py
│   ├── registry.py
│   ├── exceptions.py
│   ├── error_normalizer.py
│   ├── method_catalog.json
│   └── modules...
│
├── strategies/
│   ├── validators/
│   └── executors/
│
├── docs/
│   ├── arch/
│   ├── backend/
│   ├── error/
│   ├── modules/
│   ├── theory/
│   └── ui/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── scripts/
├── examples/
├── run.py
└── README.md
```

---

# ▶️ Running the Application

### 1. Install dependencies (Python 3.12)

```
pip install -r requirements.txt
```

### 2. Start the application

```
python .\run.py
```

Then open:

```
http://127.0.0.1:8050/
```

---

# 🖼️ Screenshots

### 🌞 Light Theme
<p align="center">
  <img src="app/assets/main-light.png" width="800">
</p>

### 🌙 Dark Theme
<p align="center">
  <img src="app/assets/main-dark.png" width="800">
</p>

---

# 🧠 Architecture Overview

NA‑Engine follows a clean, scalable architecture based on **layered contracts**.

### 🔹 Dash UI Layer
Layouts + callbacks, fully decoupled from numerical logic.

### 🔹 Core Numerical Engine
`NumericalMethod` orchestrates:
- Constructor  
- Validator  
- Executor  

### 🔹 Renderer Layer
Transforms raw results into typed payloads.

### 🔹 UIContract Layer
Builds Dash components based on payload type.

---

# 🧪 Testing Strategy

### 1. Local Unit Tests (pytest)
Validan:
- Correctitud  
- Estabilidad numérica  
- Precisión  
- Comportamiento determinista  
- Stress tests con DataFrames grandes  

### 2. Integration Tests (GitHub Actions)
Validan:
- Pipeline completo  
- Consistencia entre módulos  
- Manejo de errores  
- Estabilidad del renderer  

### 3. UI Interaction Tests (dash.testing)
Validan:
- Comportamiento dinámico  
- Callbacks  
- Renderizado  
- Manejo de tablas y uploads  

---

# 🛣️ Roadmap

- [X] Hermite & Barycentric interpolation  
- [X] Advanced ODE solvers (RK45, Adams–Bashforth)  
- [X] CI/CD pipeline  
- [X] Symbolic support (SymPy)  
- [ ] PDE solvers (Heat, Wave, Laplace)  
- [ ] Docker support  
- [ ] Django backend integration  

---

# Release Notes

### v0.1.0 — MVP
- Added dynamic documentation loader
- Added MathJax support
- Added dark/light theme for theory
- Added folder structure docs/theory/<module>/<method>.md
- Completed Stage 4

---

# 📜 License

Licensed under the **MIT License**.

---

# ✨ Author

Developed by **Axel Espinosa, M. Sc.**

---
