
---

# 📘 **README v1.1 — NA‑Engine (Python 3.12, MIT License)**

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
├── app/                         # Dash application
│   ├── __init__.py
│   ├── app.py                   # Dash initialization
│   ├── layout/                  # UI components
│   │   ├── base_layout.py
│   │   ├── interpolation_layout.py
│   │   ├── integration_layout.py
│   │   └── ode_layout.py
│   │
│   ├── callbacks/               # Dash callbacks
│   │   ├── interpolation_callbacks.py
│   │   ├── integration_callbacks.py
│   │   └── ode_callbacks.py
│   │
│   └── assets/                  # CSS, images, static files
│
├── core/                        # Numerical computation engine
│   ├── __init__.py
│   ├── base_method.py           # Abstract class for numerical methods
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
├── tests/                       # Unit tests (pytest)
│   ├── test_interpolation.py
│   ├── test_integration.py
│   └── test_ode.py
│
├── examples/                    # Example datasets (CSV/Excel)
│
├── requirements.txt
├── run.py                       # Entry point to run the Dash app
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
`http://127.0.0.1:8050/` [(127.0.0.1 in Bing)](https://www.bing.com/search?q="http%3A%2F%2F127.0.0.1%3A8050%2F")
```

Open it in your browser to use NA‑Engine.

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

- [ ] Add Hermite and Barycentric interpolation
- [ ] Add advanced ODE solvers (RK45, Adams–Bashforth)
- [ ] Add PDE solvers (Heat, Wave, Laplace)
- [ ] Add symbolic support (SymPy)
- [ ] Add CI/CD pipeline (GitLab or GitHub Actions)
- [ ] Add Docker support
- [ ] Add Django backend integration
- [ ] Improve UI/UX with custom CSS and components

---

## 📜 License — MIT

This project is licensed under the **MIT License**, allowing free use, modification, and distribution with attribution.

---

## ✨ Author

Developed by **Axel Espinosa M. Sc.**


---

