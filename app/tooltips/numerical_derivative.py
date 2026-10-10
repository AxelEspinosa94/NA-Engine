# ============================================================
# Tooltips — Numerical Derivative Module
# ============================================================

TOOLTIPS = {
    # ───────────────────────────────────────────────
    # Selector de método
    # ───────────────────────────────────────────────
    "deriv-method": (
        "Selecciona el método de derivación numérica.\n\n"
        "• Forward: usa f(x+h) para aproximar f'(x).\n"
        "• Backward: usa f(x−h).\n"
        "• Central: usa f(x+h) y f(x−h), mayor precisión.\n"
        "• Richardson: acelera la convergencia usando múltiples h.\n"
        "• 2da/3ra derivada: fórmulas de orden superior.\n"
        "• Parciales: ∂f/∂x y ∂f/∂y para funciones de dos variables."
    ),
    # ───────────────────────────────────────────────
    # Modo de entrada (siempre función)
    # ───────────────────────────────────────────────
    "deriv-input-mode": (
        "El módulo de derivación numérica solo trabaja con funciones "
        "analíticas f(x) o f(x, y). No requiere tablas ni archivos."
    ),
    # ───────────────────────────────────────────────
    # Función f(x)
    # ───────────────────────────────────────────────
    "deriv-function": (
        "Ingresa la función a derivar.\n\n"
        "Ejemplos válidos:\n"
        "• x**2 + 3*x\n"
        "• sin(x) + exp(x)\n"
        "• x**3 - 4*x + 1\n\n"
        "Puedes usar funciones de Python: sin, cos, exp, log, sqrt."
    ),
    # ───────────────────────────────────────────────
    # Valor de x
    # ───────────────────────────────────────────────
    "deriv-x": (
        "Punto donde deseas evaluar la derivada.\n\n"
        "Ejemplo: si f(x) = x² y x = 2, entonces f'(2) = 4."
    ),
    # ───────────────────────────────────────────────
    # Paso h
    # ───────────────────────────────────────────────
    "deriv-h": (
        "Tamaño del paso para la aproximación.\n\n"
        "• Valores pequeños (0.01, 0.001) dan mayor precisión.\n"
        "• Valores demasiado pequeños pueden causar error numérico.\n\n"
        "Richardson ajusta automáticamente varios valores de h."
    ),
    # ───────────────────────────────────────────────
    # Valor de y (solo parciales)
    # ───────────────────────────────────────────────
    "deriv-y": (
        "Valor de y para evaluar derivadas parciales.\n\n"
        "Ejemplo: si f(x, y) = x*y + y², puedes evaluar ∂f/∂y en (x=2, y=3)."
    ),
    # ───────────────────────────────────────────────
    # Botón Calcular
    # ───────────────────────────────────────────────
    "deriv-run-btn": (
        "Ejecuta el método seleccionado y muestra la derivada numérica.\n\n"
        "El resultado incluye:\n"
        "• Valor de la derivada\n"
        "• Explicación del método\n"
        "• Fórmula utilizada\n"
        "• Errores y advertencias si aplica"
    ),
}
