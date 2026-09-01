# ============================================================
# Tooltips — Nonlinear Equations Module
# ============================================================

TOOLTIPS = {
    # ───────────────────────────────────────────────
    # Selector de método
    # ───────────────────────────────────────────────
    "nonlin-method": (
        "Selecciona el método para resolver la ecuación no lineal f(x) = 0.\n\n"
        "• Bisección: robusto, requiere intervalo con cambio de signo.\n"
        "• Falsa Posición: similar a bisección pero más rápido.\n"
        "• Newton: muy rápido, requiere f'(x) y buen x0.\n"
        "• Secante: rápido, no requiere derivada.\n"
        "• Punto Fijo: requiere g(x) tal que x = g(x) converja."
    ),
    # ───────────────────────────────────────────────
    # Modo de entrada (siempre función)
    # ───────────────────────────────────────────────
    "nonlin-input-mode": (
        "El módulo trabaja únicamente con funciones analíticas f(x). "
        "No admite tablas ni datos discretos."
    ),
    # ───────────────────────────────────────────────
    # Función f(x)
    # ───────────────────────────────────────────────
    "nonlin-f": (
        "Ingresa la función f(x) cuya raíz deseas encontrar.\n\n"
        "Ejemplos válidos:\n"
        "• x**2 - 5\n"
        "• sin(x) - x/2\n"
        "• exp(x) - 3*x\n\n"
        "Puedes usar funciones de Python: sin, cos, exp, log, sqrt."
    ),
    # ───────────────────────────────────────────────
    # Valor inicial x0
    # ───────────────────────────────────────────────
    "nonlin-x0": (
        "Punto inicial para métodos iterativos.\n\n"
        "• Newton y Secante requieren un buen x0 para converger.\n"
        "• Punto Fijo también depende fuertemente de x0.\n"
        "• Bisección y Falsa Posición no usan x0."
    ),
    # ───────────────────────────────────────────────
    # Función g(x) — Punto Fijo
    # ───────────────────────────────────────────────
    "nonlin-g": (
        "Ingresa la función g(x) para el método de Punto Fijo.\n\n"
        "Debe cumplir:\n"
        "• x = g(x)\n"
        "• |g'(x)| < 1 cerca de la raíz para garantizar convergencia.\n\n"
        "Ejemplo: g(x) = 0.5*(x + 5/x)."
    ),
    # ───────────────────────────────────────────────
    # Valor inicial x1 — Secante
    # ───────────────────────────────────────────────
    "nonlin-x1": (
        "Segundo punto inicial para el método de Secante.\n\n"
        "La secante usa f(x0) y f(x1) para aproximar la derivada.\n"
        "Si x0 y x1 están muy cerca, la convergencia mejora."
    ),
    # ───────────────────────────────────────────────
    # Intervalo [a, b] — Bisección y Falsa Posición
    # ───────────────────────────────────────────────
    "nonlin-a": (
        "Extremo izquierdo del intervalo.\n\n"
        "Debe cumplirse f(a) * f(b) < 0 para garantizar una raíz dentro."
    ),
    "nonlin-b": (
        "Extremo derecho del intervalo.\n\n"
        "Si f(a) y f(b) tienen el mismo signo, Bisección y Falsa Posición no funcionan."
    ),
    "nonlin-interval": (
        "Intervalo [a, b] donde se busca la raíz.\n\n"
        "Debe cumplirse f(a) * f(b) < 0 para garantizar una raíz dentro."
    ),
    # ───────────────────────────────────────────────
    # Botón Calcular
    # ───────────────────────────────────────────────
    "nonlin-run-btn": (
        "Ejecuta el método seleccionado y muestra:\n"
        "• La raíz aproximada\n"
        "• Número de iteraciones\n"
        "• Error relativo\n"
        "• Tabla de iteraciones\n"
        "• Advertencias si el método no converge"
    ),
}
