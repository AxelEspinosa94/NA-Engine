# app/tooltips/ode.py

TOOLTIPS = {

    # ───────────────────────────────────────────────
    # Selector de método
    # ───────────────────────────────────────────────
    "ode-method": (
        "Selecciona el método numérico para resolver la ecuación diferencial. "
        "Los métodos IVP avanzan paso a paso desde x₀, mientras que Shooting y "
        "Diferencias Finitas resuelven problemas de frontera (BVP)."
    ),

    # ───────────────────────────────────────────────
    # Modo de entrada
    # ───────────────────────────────────────────────
    "ode-input-mode": (
        "Elige si deseas ingresar una función f(x, y) para un IVP o un sistema "
        "de ecuaciones diferenciales. Los sistemas requieren un vector inicial y₀."
    ),

    # ───────────────────────────────────────────────
    # Función f(x, y)
    # ───────────────────────────────────────────────
    "ode-function": (
        "Ingresa la ecuación diferencial en forma f(x, y). Ejemplo: x + y. "
        "NA‑Engine interpreta esta función usando sintaxis de Python."
    ),

    # ───────────────────────────────────────────────
    # Sistema de ecuaciones
    # ───────────────────────────────────────────────
    "ode-system": (
        "Define un sistema de ecuaciones diferenciales. Cada ecuación debe "
        "estar en una línea separada. Ejemplo:\n"
        "y1' = y2\n"
        "y2' = -y1"
    ),

    # ───────────────────────────────────────────────
    # Campos IVP
    # ───────────────────────────────────────────────
    "ode-ivp": "Problema de valor inicial (IVP): se conoce y(x₀) = y₀ y se busca y(x) para x > x₀.",
    "ode-x0": "Punto inicial x₀ donde comienza la integración.",
    "ode-y0": "Valor inicial y₀ de la solución en x₀.",
    "ode-x-end": "Punto final del intervalo donde se desea obtener la solución.",
    "ode-h": (
        "Paso de integración. Valores pequeños aumentan la precisión pero "
        "incrementan el costo computacional."
    ),

    # ───────────────────────────────────────────────
    # Vector inicial para sistemas
    # ───────────────────────────────────────────────
    "ode-y0-system": (
        "Vector inicial para sistemas de ecuaciones. Ejemplo: 1, 0, -2. "
        "Debe contener un valor por cada ecuación del sistema."
    ),

    # ───────────────────────────────────────────────
    # Shooting (BVP)
    # ───────────────────────────────────────────────
    "ode-shooting": "Problema de frontera (BVP) resuelto con el método Shooting. Se ajusta la pendiente inicial s₀ para cumplir la condición en x_end.",
    "ode-alpha": "Condición de frontera en x₀: α = y(x₀).",
    "ode-beta": "Condición de frontera en x_end: β = y(x_end).",
    "ode-s0": (
        "Pendiente inicial s₀ usada para disparar la solución en el método Shooting. "
        "NA‑Engine ajusta s₀ para cumplir la condición en x_end."
    ),

    # ───────────────────────────────────────────────
    # Diferencias finitas (BVP)
    # ───────────────────────────────────────────────
    "ode-fd": "Problema de frontera (BVP) resuelto con el método de diferencias finitas. Se discretiza el intervalo y se resuelve un sistema lineal.",
    "ode-alpha-fd": "Condición de frontera en x₀ para el método de diferencias finitas.",
    "ode-beta-fd": "Condición de frontera en x_end para diferencias finitas.",
    "ode-n": (
        "Número de subdivisiones del intervalo. A mayor n, mayor precisión "
        "pero mayor costo computacional."
    ),

    # ───────────────────────────────────────────────
    # Botón de ejecución
    # ───────────────────────────────────────────────
    "ode-run-btn": (
        "Ejecuta el método seleccionado con los parámetros proporcionados. "
        "El resultado se mostrará en la sección inferior."
    ),
}
