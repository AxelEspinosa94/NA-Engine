# ============================================================
# Tooltips — Linear Algebra Module
# ============================================================

TOOLTIPS = {
    # ───────────────────────────────────────────────
    # Tipo de operación
    # ───────────────────────────────────────────────
    "la-calculation-type": (
        "Selecciona el tipo de cálculo que deseas realizar.\n\n"
        "• Operaciones con matrices: determinante, inversa, norma, etc.\n"
        "• Sistema de ecuaciones: resolver Ax = b con métodos directos o iterativos."
    ),
    # ───────────────────────────────────────────────
    # Método
    # ───────────────────────────────────────────────
    "la-calculation-mode": (
        "Selecciona el método o la operación a aplicar.\n\n"
        "Operaciones con matrices:\n"
        "• Determinante: calcula det(A).\n"
        "• Inversa: calcula A⁻¹ si existe.\n"
        "• Norma: norma matricial.\n"
        "• Número de condición: cond(A).\n"
        "• Transpuesta: Aᵀ.\n"
        "• Rango: número de columnas linealmente independientes.\n\n"
        "Sistemas Ax = b:\n"
        "• Gauss: eliminación simple.\n"
        "• Gauss-Jordan: reducción completa.\n"
        "• LU: factorización A = LU.\n"
        "• Cholesky: para matrices simétricas y definidas positivas.\n"
        "• QR: factorización ortogonal.\n"
        "• Jacobi: método iterativo.\n"
        "• Gauss-Seidel: iterativo, usualmente más rápido que Jacobi."
    ),
    # ───────────────────────────────────────────────
    # Modo de entrada
    # ───────────────────────────────────────────────
    "la-input-mode": (
        "Selecciona cómo deseas ingresar la matriz A (y el vector b si aplica).\n\n"
        "• Subir archivo: acepta .txt, .csv y .xlsx.\n"
        "• Tabla manual: ingresa los valores directamente en la tabla."
    ),
    # ───────────────────────────────────────────────
    # Upload de archivo
    # ───────────────────────────────────────────────
    "la-upload": (
        "Sube un archivo que contenga la matriz A (y opcionalmente el vector b).\n\n"
        "Formatos soportados:\n"
        "• .txt — valores separados por espacios.\n"
        "• .csv — valores separados por comas.\n"
        "• .xlsx — hoja de cálculo.\n\n"
        "El sistema detecta automáticamente si el archivo incluye el vector b."
    ),
    # ───────────────────────────────────────────────
    # Tabla manual — Matriz A
    # ───────────────────────────────────────────────
    "la-table-A": (
        "Ingresa manualmente la matriz A.\n\n"
        "• Puedes editar cualquier celda.\n"
        "• Puedes eliminar filas.\n"
        "• El tamaño de la matriz determina el tamaño del sistema Ax = b."
    ),
    # ───────────────────────────────────────────────
    # Vector b
    # ───────────────────────────────────────────────
    "la-vector-b": (
        "Ingresa el vector b para el sistema Ax = b.\n\n"
        "Formato:\n"
        "• Valores separados por espacios: ej. '1 2 3'.\n"
        "• Debe tener la misma cantidad de elementos que filas tenga A."
    ),
    # ───────────────────────────────────────────────
    # Botón Calcular
    # ───────────────────────────────────────────────
    "la-run-btn": (
        "Ejecuta el método seleccionado.\n\n"
        "El resultado puede incluir:\n"
        "• Matrices factorizadas (LU, QR, etc.)\n"
        "• Solución del sistema Ax = b\n"
        "• Determinante, inversa, rango, norma\n"
        "• Iteraciones para métodos iterativos\n"
        "• Advertencias si la matriz es singular o mal condicionada"
    ),
}
