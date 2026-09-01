# ============================================================
# Tooltips — Numerical Integration Module
# ============================================================

TOOLTIPS = {
    # ───────────────────────────────────────────────
    # Selector de método
    # ───────────────────────────────────────────────
    "integr-method": (
        "Selecciona el método de integración numérica.\n\n"
        "• Trapecio Simple: una sola aplicación del método.\n"
        "• Trapecio Compuesto: divide el intervalo en n subintervalos.\n"
        "• Simpson 1/3: usa parábolas; requiere n par.\n"
        "• Simpson 3/8: usa cúbicas; requiere n múltiplo de 3.\n"
        "• Romberg: extrapolación de Richardson sobre Trapecio.\n"
        "• Gauss-Legendre: cuadratura de alta precisión con puntos óptimos."
    ),
    # ───────────────────────────────────────────────
    # Modo de entrada (siempre función)
    # ───────────────────────────────────────────────
    "integr-input-mode": (
        "El módulo trabaja únicamente con funciones analíticas f(x). "
        "No admite tablas ni datos discretos."
    ),
    # ───────────────────────────────────────────────
    # Función f(x)
    # ───────────────────────────────────────────────
    "integr-fn": (
        "Ingresa la función f(x) que deseas integrar.\n\n"
        "Ejemplos válidos:\n"
        "• sin(x) + x**2\n"
        "• exp(-x**2)\n"
        "• log(x + 1)\n\n"
        "Puedes usar funciones de Python: sin, cos, exp, log, sqrt."
    ),
    # ───────────────────────────────────────────────
    # Intervalo [a, b]
    # ───────────────────────────────────────────────
    "integr-a": (
        "Extremo izquierdo del intervalo de integración.\n\n"
        "Debe ser menor que b para métodos estándar."
    ),
    "integr-b": (
        "Extremo derecho del intervalo de integración.\n\n"
        "Si a > b, el resultado será negativo (integración invertida)."
    ),
    # ───────────────────────────────────────────────
    # Número de subintervalos (n)
    # ───────────────────────────────────────────────
    "integr-n": (
        "Número de subintervalos para métodos compuestos.\n\n"
        "• Trapecio Compuesto: cualquier n.\n"
        "• Simpson 1/3: n debe ser par.\n"
        "• Simpson 3/8: n debe ser múltiplo de 3.\n\n"
        "Valores grandes de n aumentan la precisión pero también el costo."
    ),
    # ───────────────────────────────────────────────
    # Puntos de Gauss-Legendre
    # ───────────────────────────────────────────────
    "integr-gauss-points": (
        "Número de puntos para la cuadratura de Gauss-Legendre.\n\n"
        "• 2 puntos: precisión alta para polinomios hasta grado 3.\n"
        "• 3 puntos: precisión para polinomios hasta grado 5.\n"
        "• 4 puntos o más: excelente precisión para funciones suaves.\n\n"
        "Los puntos y pesos se calculan automáticamente."
    ),
    # ───────────────────────────────────────────────
    # Botón Calcular
    # ───────────────────────────────────────────────
    "integr-run-btn": (
        "Ejecuta el método seleccionado y muestra:\n"
        "• Valor aproximado de la integral\n"
        "• Tabla de iteraciones (si aplica)\n"
        "• Error estimado\n"
        "• Detalles del método\n"
        "• Advertencias si el método no es aplicable"
    ),
}
