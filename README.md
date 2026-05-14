<p align="center">

  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-Dash-0099ff?logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
  <img src="https://img.shields.io/badge/Assets-AI%20Generated-ff69b4?logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-pytest-blueviolet" />
  <img src="https://img.shields.io/badge/Domain-Numerical%20Analysis-orange" />

</p>

---

# 📘 **README v1.2 — NA‑Engine (Python 3.12, MIT License)**

# NA‑Engine
NA‑Engine is a modular, extensible, and interactive engine for solving Numerical Methods, Numerical Analysis, and Differential Equations problems.  
Built with Python **3.12** and powered by Dash, it provides automated computations, mathematical rendering, and structured outputs for academic, scientific, and engineering use.

---

## 🚀 Features

- Interactive Dash web application
- Numerical Methods:
  - Interpolation (Newton, Lagrange, Splines)
  - Numerical Integration (Simpson, Trapezoidal)
  - Differential Equations (Euler, Runge–Kutta, Systems)
- Markdown‑based mathematical output
- Modular OOP architecture for numerical algorithms
- Ready for unit testing with `pytest`
- Clean separation between UI, callbacks, and computation logic
- Expandable structure for new numerical methods and solvers

---

## 📁 Repository Structure

```
NA-Engine/
│
├── app/                         
│   ├── __init__.py
│   ├── app.py                   
│   ├── layout/                  
│   │   ├── base_layout.py
│   │   ├── home_layout.py
│   │   ├── interpolation_layout.py
│   │   ├── integration_layout.py
│   │   ├── navigation_layout.py
│   │   └── ode_layout.py
│   │
│   ├── callbacks/               
│   │   ├── integration_callbacks.py
│   │   ├── interpolation_callbacks.py
│   │   ├── navigation_callbacks.py
│   │   ├── ode_callbacks.py
│   │   └── theme_callbacks.py
│   │
│   └── assets/                  
│       ├── base.css
│       ├── components.css
│       ├── dark.css
│       ├── layout.css
│       ├── responsive.css
│       ├── theme.css
│       ├── hero2.png
│       ├── puma3.png
│       └── puma4.png
│
├── core/                        
│   ├── __init__.py
│   ├── base_method.py           
│   ├── registry.py              # <-- JSON catalog loader
│   ├── exceptions.py            # <-- Fine Exceptions
│   ├── method_catalog.json      # <-- Method catalog
│   │
│   ├── interpolation/
│   │   ├── newton.py
│   │   ├── lagrange.py
│   │   └── splines.py
│   │
│   ├── integration/
│   │   ├── simpson.py
│   │   └── trapezoidal.py
│   │
│   └── ode/
│       ├── euler.py
│       ├── runge_kutta.py
│       └── systems.py
│
├── strategies/                  # <-- NUEVO: validators, executors, formatters
│   ├── __init__.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── interpolation_validators.py
│   │   ├── integration_validators.py
│   │   └── ode_validators.py
│   │
│   ├── executors/
│   │   ├── __init__.py
│   │   ├── interpolation_executors.py
│   │   ├── integration_executors.py
│   │   └── ode_executors.py
│   │
│   └── formatters/
│       ├── __init__.py
│       └── table_formatter.py
│
├── tests/                       
│   ├── test_interpolation.py
│   ├── test_integration.py
│   └── test_ode.py
│
├── examples/                    
│
├── requirements.txt
├── run.py                       
└── README.md

```

---

## ▶️ Running the Application

### **1. Install dependencies (Python 3.12)**

```
pip install -r requirements.txt
```

### **2. Start the application**

```
python run.py
```

The app will start locally and provide a URL such as:

```
`http://127.0.0.1:8050/`
```

Open it in your browser to use NA‑Engine.

---

## 🖼️ Screenshots

Below are previews of the NA‑Engine interface in both **light** and **dark** themes.

### 🌞 Light Theme

<p align="center">
  <img src="app/assets/main-light.png" width="800">
</p>

<p align="center">
  <img src="app/assets/main-light-1.png" width="800">
</p>


<p align="center">
  <img src="app/assets/main-light-2.png" width="800">
</p>


### 🌙 Dark Theme

<p align="center">
  <img src="app/assets/main-dark.png" width="800">
</p>

<p align="center">
  <img src="app/assets/main-dark-1.png" width="800">
</p>


<p align="center">
  <img src="app/assets/main-dark-2.png" width="800">
</p>

---

## Core Calculator UML Diagram
```mermaid
classDiagram
    class NumericalMethod {
        - method: str
        - input: dict
        - kwargs: dict
        - catalog: dict
        + validate_input() bool
        + execute() Any
        + format_output(result) dict
    }

    class MethodRegistry {
        + load_catalog() dict
        + get_method_info(method: str) dict
    }

    class BaseValidator {
        <<interface>>
        + validate(input_data: dict) bool
    }

    class BaseExecutor {
        <<interface>>
        + run(instance: Any) Any
    }

    class NewtonInterpolation
    class NewtonInputValidator
    class NewtonExecutor

    NumericalMethod --> MethodRegistry : uses
    NumericalMethod --> BaseValidator : composes
    NumericalMethod --> BaseExecutor : composes

    NewtonInputValidator ..|> BaseValidator
    NewtonExecutor ..|> BaseExecutor
```

---

### 📌 Notes



---

## 🧠 Architecture Overview

NA‑Engine follows a clean, scalable architecture:

### **Dash UI Layer**
Layouts and callbacks separated by module for clarity and maintainability.

### **Core Numerical Engine**
Each numerical method is implemented as a class inheriting from `NumericalMethod`, enabling:

- Polymorphism  
- Reusability  
- Testability  
- Extensibility  

### **Testing Layer**
`pytest`‑based unit tests ensure correctness and prevent regressions as the engine grows.

---

## 🛣️ Roadmap

- [X] Improve UI/UX with custom CSS and components
- [ ] Add Hermite and Barycentric interpolation
- [ ] Add advanced ODE solvers (RK45, Adams–Bashforth)
- [ ] Add PDE solvers (Heat, Wave, Laplace)
- [ ] Add symbolic support (SymPy)
- [ ] Add CI/CD pipeline (GitLab or GitHub Actions)
- [ ] Add Docker support
- [ ] Add Django backend integration


---

## 📜 License — MIT

This project is licensed under the **MIT License**, allowing free use, modification, and distribution with attribution.

---

## ✨ Author

Developed by **Axel Espinosa M. Sc.**


---

