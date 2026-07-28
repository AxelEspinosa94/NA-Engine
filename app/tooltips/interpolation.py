# ============================================================
# Tooltips — Numerical Interpolation Module
# ============================================================

TOOLTIPS = {

    # ───────────────────────────────────────────────
    # Selector de método
    # ───────────────────────────────────────────────
    "interp-method": (
        "Selecciona el método de interpolación.\n\n"
        "• Lagrange: polinomio global, fácil de implementar.\n"
        "• Newton: usa diferencias divididas, eficiente para agregar puntos.\n"
        "• Hermite: interpola valores y derivadas.\n"
        "• Splines Cúbicos: curvas suaves por tramos, excelente estabilidad."
    ),

    # ───────────────────────────────────────────────
    # Modo de entrada
    # ───────────────────────────────────────────────
    "interp-input-mode": (
        "Selecciona cómo deseas ingresar los datos para construir la interpolación.\n\n"
        "• Función f(x): genera puntos automáticamente en un rango.\n"
        "• Tabla manual: ingresa puntos (x, y) directamente.\n"
        "• Subir archivo: carga datos desde .csv o .txt."
    ),

    # ───────────────────────────────────────────────
    # Función f(x)
    # ───────────────────────────────────────────────
    "interp-fn": (
        "Ingresa la función f(x) que deseas interpolar.\n\n"
        "Ejemplos válidos:\n"
        "• x**2 + 1\n"
        "• sin(x)\n"
        "• exp(-x)\n\n"
        "Puedes usar funciones de Python: sin, cos, exp, log, sqrt."
    ),

    # ───────────────────────────────────────────────
    # Rango [a, b]
    # ───────────────────────────────────────────────
    "interp-a": (
        "Extremo izquierdo del rango donde se generarán los puntos de interpolación."
    ),

    "interp-b": (
        "Extremo derecho del rango.\n\n"
        "El sistema generará n puntos equiespaciados entre a y b."
    ),

    # ───────────────────────────────────────────────
    # Número de puntos
    # ───────────────────────────────────────────────
    "interp-n": (
        "Cantidad de puntos a generar para la interpolación.\n\n"
        "• Más puntos → mayor precisión pero polinomios más inestables.\n"
        "• Splines no sufren inestabilidad por muchos puntos."
    ),

    # ───────────────────────────────────────────────
    # Upload de archivo
    # ───────────────────────────────────────────────
    "interp-upload": (
        "Sube un archivo con los puntos (x, y) para interpolar.\n\n"
        "Formatos soportados:\n"
        "• .csv — columnas x,y\n"
        "• .txt — valores separados por espacios o comas\n\n"
        "El sistema detecta automáticamente el formato."
    ),

    # ───────────────────────────────────────────────
    # Tabla manual
    # ───────────────────────────────────────────────
    "interp-table": (
        "Ingresa manualmente los puntos (x, y) para la interpolación.\n\n"
        "• Puedes editar cualquier celda.\n"
        "• Puedes eliminar filas.\n"
        "• Se requiere al menos 2 puntos para interpolar."
    ),

    # ───────────────────────────────────────────────
    # Valor a evaluar (xk)
    # ───────────────────────────────────────────────
    "interp-xk": (
        "Punto donde deseas evaluar el polinomio o spline interpolante.\n\n"
        "Ejemplo: si xk = 1.5, el sistema calcula P(1.5)."
    ),

    # ───────────────────────────────────────────────
    # Botón Calcular
    # ───────────────────────────────────────────────
    "interp-run-btn": (
        "Ejecuta el método seleccionado y muestra:\n"
        "• Polinomio o spline resultante\n"
        "• Tabla de diferencias divididas (Newton)\n"
        "• Coeficientes del spline cúbico\n"
        "• Evaluación en xk\n"
        "• Gráfica opcional del interpolante"
    ),
}
