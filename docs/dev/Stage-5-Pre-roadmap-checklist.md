
---

# 🧩 **Stage 5 — Módulo ODE (Enhancement & Expansion)**  
### *Complemento del Roadmap General — NA‑Engine*

El módulo de **Ecuaciones Diferenciales Ordinarias (ODE)** completado en Stage 4 ya cuenta con:

- Constructor validado  
- Validator estricto  
- Executor completo (IVP, sistemas, BVP)  
- Layout funcional  
- Callbacks dinámicos  
- Stress tests iniciales  

Para Stage 5, se requiere una expansión y refinamiento profundo en tres áreas:

- **UI/UX**  
- **Homologación de inputs y estilos**  
- **Expansión funcional del módulo ODE**  

---

# 🎨 **Prioridad Alta — UI/UX del módulo ODE**

## **1. Homologación visual de inputs**
- [ ] Unificar estilos de todos los inputs del módulo ODE:
  - [ ] Inputs numéricos  
  - [ ] Textareas  
  - [ ] Dropdowns  
  - [ ] RadioItems  
- [ ] Asegurar consistencia con:
  - [ ] Derivadas  
  - [ ] Integración  
  - [ ] Álgebra Lineal  
  - [ ] No Lineales  
- [ ] Crear un **input style registry** para NA‑Engine:
  - [ ] Colores  
  - [ ] Bordes  
  - [ ] Padding  
  - [ ] Placeholders  
  - [ ] Tamaños  
- [ ] Homologar mensajes de error visuales:
  - [ ] Borde rojo  
  - [ ] Tooltip  
  - [ ] Bloque de error del UIContract  

---

## **2. Pulido de UI del módulo ODE**
- [ ] Añadir imágenes ilustrativas para cada método:
  - [ ] Euler  
  - [ ] Heun  
  - [ ] RK2  
  - [ ] RK4  
  - [ ] Adams family  
  - [ ] RK4 System  
  - [ ] Shooting  
  - [ ] Finite Differences  
- [ ] Añadir captions específicos:
  - [ ] “Método de Euler — IVP”  
  - [ ] “Método de Runge–Kutta 4 — IVP”  
  - [ ] “Sistema de ODE — RK4”  
  - [ ] “Método de Shooting — BVP”  
  - [ ] “Diferencias Finitas — BVP”  
- [ ] Añadir bloques visuales:
  - [ ] Expresión simbólica del método  
  - [ ] Tabla de iteraciones (cuando aplique)  
  - [ ] Gráfica de trayectoria  
  - [ ] Gráfica de error (opcional)  
- [ ] Añadir tooltips explicativos:
  - [ ] ¿Qué es un IVP?  
  - [ ] ¿Qué es un BVP?  
  - [ ] ¿Qué es un sistema de ODE?  
  - [ ] ¿Qué significa h?  

---

## **3. Mejoras en el layout**
- [ ] Reorganizar tarjetas:
  - [ ] Inputs IVP  
  - [ ] Inputs Sistema  
  - [ ] Inputs Shooting  
  - [ ] Inputs Finite Differences  
- [ ] Añadir secciones plegables (collapsible):
  - [ ] “Datos del problema”  
  - [ ] “Opciones avanzadas”  
  - [ ] “Resultados”  
- [ ] Añadir un bloque de “Resumen del método seleccionado”.

---

# 🧠 **Prioridad Alta — Expansión funcional del módulo ODE**

## **4. Nuevos métodos IVP**
- [ ] Añadir **RKF45 (Runge–Kutta–Fehlberg)**  
- [ ] Añadir **Dormand–Prince (RKDP)**  
- [ ] Añadir **Métodos adaptativos (h dinámico)**  
- [ ] Añadir **Métodos para ODE rígidas (stiff ODEs)**:
  - [ ] Backward Euler  
  - [ ] Crank–Nicolson  
  - [ ] Implicit RK  

---

## **5. Expansión del módulo de sistemas**
- [ ] Añadir soporte para:
  - [ ] Sistemas grandes (n > 10)  
  - [ ] Sistemas acoplados no lineales  
  - [ ] Sistemas rígidos  
- [ ] Añadir visualización:
  - [ ] Gráficas múltiples  
  - [ ] Fase (phase portrait)  
  - [ ] Trayectorias en 3D  

---

## **6. Expansión del módulo BVP**
- [ ] Shooting avanzado:
  - [ ] Ajuste automático de pendiente  
  - [ ] Métodos de corrección (secante para s0)  
- [ ] Finite Differences avanzado:
  - [ ] Soporte para ecuaciones no lineales  
  - [ ] Soporte para condiciones de frontera mixtas  
  - [ ] Soporte para mallas no uniformes  

---

# 🟨 **Prioridad Media — Documentación y teoría ODE**

## **7. Documentación integrada**
- [ ] Crear módulo de teoría ODE:
  - [ ] IVP  
  - [ ] BVP  
  - [ ] Sistemas  
  - [ ] Métodos RK  
  - [ ] Métodos multistep  
  - [ ] Métodos implícitos  
- [ ] Integrar con `dcc.Markdown`  
- [ ] Añadir ejemplos interactivos:
  - [ ] “Ejemplo RK4”  
  - [ ] “Ejemplo Shooting”  
  - [ ] “Ejemplo Finite Differences”  

---

# 🟦 **Prioridad Baja — Stage 6**

## **8. Input Mode Table → ODE**
- [ ] Permitir input_mode `table` para ODE:
  - [ ] Cargar tabla de puntos (x, y)  
  - [ ] Ajustar polinomio interpolante  
  - [ ] Resolver ODE inversa (opcional)  

---

# 🏁 **Conclusión — Módulo ODE Stage 5**

El módulo ODE en Stage 5 se enfocará en:

- **Pulir la UI**  
- **Homologar inputs y estilos**  
- **Mejorar captions y bloques visuales**  
- **Añadir métodos avanzados (RKF45, adaptativos, stiff)**  
- **Expandir sistemas y BVP**  
- **Integrar teoría y documentación**  

Con esto, NA‑Engine quedará listo para:

- resolver ODE avanzadas  
- manejar sistemas grandes  
- resolver BVP complejos  
- ofrecer una UI profesional y homogénea  
- preparar Stage 6 (interpolación → ODE → integración)

---

