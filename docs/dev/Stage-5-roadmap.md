
---

# 🧩 **ROADMAP — STAGE 5**  
### *Enhancement & Expansion — NA‑Engine*

---

# 🎨 **A. UI/UX Global**

## **1. Homologación visual de inputs**
- [ ] Inputs numéricos  
- [ ] Textareas  
- [ ] Dropdowns  
- [ ] RadioItems  
- [ ] Botones  
- [ ] Input Style Registry global  
- [ ] Mensajes de error homogéneos  
- [ ] Estados visuales (hover, error, disabled)

## **2. Tooltip System**
- [ ] Identificar elementos  
- [ ] Crear `tooltip_input()`  
- [ ] Crear `tooltip_icon()`  
- [ ] Hover/click interactions  
- [ ] Estilos para modo claro/oscuro  
- [ ] Integración en todos los módulos

## **3. Homologación de idioma (base en inglés)**
- [ ] Migrar UI visible a inglés  
- [ ] Migrar captions a inglés  
- [ ] Migrar tooltips a inglés  
- [ ] Migrar documentación a inglés  
- [ ] Preparar estructura i18n (sin callbacks)

## **4. Pulido de UI**
- [ ] Imágenes ilustrativas por método  
- [ ] Captions específicos  
- [ ] Bloques visuales (fórmulas, tablas, gráficas)  
- [ ] Tooltips explicativos  
- [ ] Auto‑captions desde JSON

## **5. Responsiveness**
- [ ] Layout responsive  
- [ ] Cards adaptables  
- [ ] Inputs fluidos  
- [ ] Gráficas responsivas  
- [ ] Mobile-friendly UI

## **6. Loading Indicators**
- [ ] Indicadores para cálculos pesados  
- [ ] Indicadores para ODE  
- [ ] Indicadores para integración  
- [ ] Indicadores para álgebra lineal

## **7. Exportación de resultados**
- [ ] Exportar tablas  
- [ ] Exportar gráficas  
- [ ] Exportar logs  
- [ ] Exportar reportes (PDF/HTML)

## **8. Persistencia de usuario**
- [ ] Guardar inputs  
- [ ] Guardar preferencias  
- [ ] Guardar último método usado  
- [ ] Guardar idioma preferido (pre‑i18n)

---

# 🧠 **B. Expansión funcional (Todos los módulos)**

## **9. Nuevos métodos — No Lineales**
- [ ] Ridder  
- [ ] Müller  
- [ ] Brent–Dekker  
- [ ] Soporte vectorial

## **10. Nuevos métodos — Integración**
- [ ] Clenshaw–Curtis  
- [ ] Montecarlo  
- [ ] Cuadratura Adaptativa  
- [ ] Romberg Avanzado  

## **11. Nuevos métodos — ODE**
- [ ] RKF45  
- [ ] Dormand–Prince  
- [ ] Métodos adaptativos  
- [ ] Métodos rígidos (Backward Euler, Crank–Nicolson, Implicit RK)

## **12. Expansión de Sistemas ODE**
- [ ] Sistemas grandes  
- [ ] Sistemas acoplados  
- [ ] Sistemas rígidos  
- [ ] Phase portrait  
- [ ] Trayectorias 3D

## **13. Expansión BVP**
- [ ] Shooting avanzado  
- [ ] Finite Differences avanzado  
- [ ] Mallas no uniformes  
- [ ] Condiciones mixtas  

---

# 🟨 **C. Documentación**

## **14. Documentación integrada**
- [ ] Teoría ODE  
- [ ] Teoría No Lineales  
- [ ] Teoría Integración  
- [ ] Teoría Interpolación  
- [ ] Ejemplos interactivos  
- [ ] Migración a inglés

---

# 🟦 **D. Gantt Chart**

## Enhancement & Expansion — NA‑Engine

**Duración estimada:** 10–14 semanas
**Dependencias:** Stage 4 completado
**Paralelizable:** Sí, casi todo excepto ODE avanzado

```gantt
    dateFormat  YYYY-MM-DD
    title Stage 5 — Enhancement & Expansion (NA‑Engine)
    excludes weekends

    section UI/UX Global
    Homologación visual de inputs        :a1, 2026-07-24, 14d
    Tooltip System                        :a2, after a1, 10d
    Homologación de idioma (base inglés)  :a3, after a2, 10d
    Pulido de UI (captions, imágenes)     :a4, after a3, 14d
    Responsiveness (mobile-friendly)      :a5, after a4, 10d
    Loading Indicators                     :a6, after a4, 7d
    Exportación de resultados              :a7, after a6, 10d
    Persistencia de usuario                :a8, after a7, 7d

    section Expansión Funcional — No Lineales
    Ridder                                 :b1, 2026-08-01, 5d
    Müller                                 :b2, after b1, 5d
    Brent–Dekker                           :b3, after b2, 5d
    Funciones vectoriales                  :b4, after b3, 7d

    section Expansión Funcional — Integración
    Clenshaw–Curtis                        :c1, 2026-08-10, 7d
    Montecarlo                             :c2, after c1, 5d
    Cuadratura Adaptativa                  :c3, after c2, 7d
    Romberg Avanzado                       :c4, after c3, 7d

    section Expansión Funcional — ODE
    RKF45                                  :d1, 2026-08-15, 10d
    Dormand–Prince                         :d2, after d1, 10d
    Métodos adaptativos (h dinámico)       :d3, after d2, 14d
    Métodos rígidos                        :d4, after d3, 14d

    section ODE — Sistemas y BVP
    Sistemas grandes                       :e1, 2026-09-01, 10d
    Sistemas acoplados                     :e2, after e1, 10d
    Sistemas rígidos                       :e3, after e2, 10d
    Phase portrait                         :e4, after e3, 7d
    Trayectorias 3D                        :e5, after e4, 7d

    Shooting avanzado                       :f1, 2026-09-20, 10d
    Finite Differences avanzado             :f2, after f1, 14d
    Mallas no uniformes                     :f3, after f2, 7d
    Condiciones mixtas                      :f4, after f3, 7d

    section Documentación
    Teoría ODE                              :g1, 2026-09-25, 14d
    Teoría No Lineales                      :g2, after g1, 10d
    Teoría Integración                      :g3, after g2, 10d
    Teoría Interpolación                    :g4, after g3, 10d
    Ejemplos interactivos                   :g5, after g4, 14d

    section Preparación Stage 6
    Estructura i18n                         :h1, 2026-10-20, 10d
    JSON global (en/es)                     :h2, after h1, 7d
    Selector de idioma (sin callbacks)      :h3, after h2, 5d
    Input Mode Table (preparación)          :h4, after h3, 10d
```

---

# 🟦 **E. Preparación Stage 6**

## **15. i18n completo (Stage 6)**
- [ ] LanguageProvider  
- [ ] JSON global  
- [ ] Traducción dinámica  
- [ ] Selector de idioma con callbacks  
- [ ] Traducción de documentación  
- [ ] Traducción de tooltips  
- [ ] Traducción de captions  

## **16. Input Mode Table → ODE (Stage 6)**
- [ ] Tabla de puntos  
- [ ] Ajuste interpolante  
- [ ] ODE inversa  

---
