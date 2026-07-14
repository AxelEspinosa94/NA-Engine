# 🧩 Stage 5 — Enhancement & Expansion Checklist
### NA‑Engine Roadmap (Post Stage 4)

Este documento describe las mejoras, refactorizaciones y extensiones que deben realizarse al inicio del Stage 5, basadas en los módulos ya adaptados durante Stage 4.

---

# ✅ Prioridad Alta — Inicio de Stage 5

## 1. Renderer / UIContract — Captions por módulo
- [ ] Crear un caption registry por módulo.
- [ ] Reemplazar el caption genérico “Polinomio”.
- [ ] Asegurar que cada módulo tenga su propio título y descripción.
- [ ] Integrar captions en todos los bloques del UIContract.

---

## 2. Derivadas — Generalización de orden
- [ ] Unificar forward/backward/central/second/third en un solo método.
- [ ] Añadir `order` a `input_data`.
- [ ] Implementar selección automática de stencil según `order`.
- [ ] Ajustar constructor y validator para soportar orden arbitrario.
- [ ] Actualizar documentación y layout.

---

## 3. Derivadas — Variables múltiples y parciales generalizadas
- [ ] Permitir variables de `a` a `z`.
- [ ] Detectar variables automáticamente con regex.
- [ ] Validar que la función solo use variables detectadas.
- [ ] Implementar derivadas parciales para cualquier variable.
- [ ] Implementar Jacobiano:
  - [ ] Derivar respecto a cada variable.
  - [ ] Devolver matriz Jacobiana.
  - [ ] Integrar con UIContract (tabla o matriz).

---

## 4. Álgebra Lineal — Estilización de vectores y matrices
- [ ] Reemplazar listas `<ul>` por DataTables verticales.
- [ ] Mostrar matrices finales (L, U, Q, R).
- [ ] Evitar mostrar pasos intermedios (costoso).
- [ ] Añadir bloques visuales para factorizaciones.

---

## 5. Álgebra Lineal — Nuevos calculation_modes
- [ ] Añadir:
  - [ ] `eigenvalues`
  - [ ] `eigenvectors`
  - [ ] `svd`
  - [ ] `linear_transform`
- [ ] Integrar validación y ejecución.
- [ ] Añadir soporte en UIContract.

---

# 🟨 Prioridad Media — Mitad de Stage 5

## 6. Derivadas — Mejorar normalización de funciones
- [ ] Expandir lista de funciones soportadas.
- [ ] Añadir soporte para:
  - [ ] `abs`, `sign`, `floor`, `ceil`
  - [ ] funciones hiperbólicas
  - [ ] funciones inversas
- [ ] Integrar parser centralizado.

---

## 7. Álgebra Lineal — Transformaciones lineales visuales
- [ ] Crear bloque visual opcional para transformaciones.
- [ ] Mostrar efecto sobre vectores base.
- [ ] Integrar con Plotly.

---

# 🟦 Prioridad Baja — Final de Stage 5 o Stage 6

## 8. Input Mode Table → Interpolación → Derivada/Integración
- [ ] Añadir input_mode `table` al módulo de Derivadas.
- [ ] Integrar con módulo de Interpolación.
- [ ] Generar polinomio interpolante.
- [ ] Derivar o integrar el polinomio.
- [ ] Validar estabilidad para polinomios de grado alto.

---

## 9. Documentación Teórica Integrada
- [ ] Crear módulo de documentación.
- [ ] Integrar archivos `.md` del repo.
- [ ] Renderizar con `dcc.Markdown`.
- [ ] Añadir navegación entre temas.
- [ ] Añadir ejemplos interactivos.

---

# 🏁 Conclusión

Este checklist define el trabajo del Stage 5:

- Refactorización profunda de Derivadas.  
- Extensión de Álgebra Lineal.  
- Mejoras de UX en Renderer/UIContract.  
- Preparación para los módulos finales:  
  - Sistemas de ecuaciones no lineales  
  - Ecuaciones diferenciales (el “final boss”)  

Las tareas de prioridad baja pueden moverse al Stage 6 sin afectar el avance del proyecto.

