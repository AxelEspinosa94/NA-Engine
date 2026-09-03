
---

# 📘 **CONTRIBUTING — NA‑Engine (Professional Edition)**


# Contributing to NA‑Engine

Gracias por tu interés en contribuir a **NA‑Engine**, un motor modular para análisis numérico con arquitectura limpia, UI/UX consistente y un sistema de renderizado avanzado.  
Este documento describe el flujo de trabajo, estándares y prácticas recomendadas para colaborar en el proyecto.

---

## 🧱 1. Requisitos del entorno

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### WSL / Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
python app.py
```

---

## 🌿 2. Flujo de trabajo con branches (Git Flow simplificado)

NA‑Engine utiliza un flujo de trabajo basado en ramas para mantener orden, estabilidad y claridad en el historial del proyecto.

### Ramas principales
- **main** → Código estable y versiones liberadas.
- **qa** → Control de calidad y validación
- **dev** → Integración de nuevas funcionalidades antes del release.

### Ramas de trabajo
- **feature/** → Nuevas funcionalidades.
- **fix/** → Correcciones específicas.
- **hotfix/** → Parches urgentes para main.
- **release/** → Preparación de versiones (tags, changelog, documentación).

Ejemplos:
```
feature/stage5-renderer
feature/output-tooltips
fix/makefile-crossplatform
release/v0.1.5
```

---

## ✏️ 3. Estándares de commits (Conventional Commits)

Usamos el estándar **Conventional Commits** para mantener un historial claro y legible.

### Tipos permitidos
- `feat:` → Nueva funcionalidad
- `fix:` → Corrección de bug
- `refactor:` → Cambio interno sin alterar funcionalidad
- `docs:` → Documentación
- `style:` → Cambios de formato o estilo
- `test:` → Pruebas
- `build:` → Makefile, dependencias, CI/CD
- `chore:` → Mantenimiento general

### Ejemplos
```
feat(renderer): add matrix group LaTeX support
fix(contract): correct multi-block dispatch for matrix outputs
style(ui): unify header gradient and spacing
build(makefile): add cross-platform arithmetic for Windows
```

---

## 🛠️ 4. Cómo trabajar en una nueva funcionalidad

1. Crear una rama desde `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/nombre-de-tu-feature
   ```

2. Hacer commits siguiendo Conventional Commits.

3. Mantener la rama enfocada en un solo objetivo.

4. Actualizar documentación si aplica.

5. Asegurarse de que la aplicación corre sin errores.

---

## 🔀 5. Cómo hacer un Merge Request hacia `main` (muy importante)

Aunque seas tú solo, este flujo te mantiene ordenado y evita romper la rama estable.

### Paso 1 — Asegúrate de que tu branch está actualizada
```bash
git checkout feature/tu-feature
git pull origin develop
```

### Paso 2 — Fusiona cambios recientes de develop
```bash
git merge develop
```

Resuelve conflictos si aparecen.

### Paso 3 — Empuja tu branch al remoto
```bash
git push origin feature/tu-feature
```

### Paso 4 — Crear el Merge Request (Pull Request)
En GitHub:

- Base branch: **main**
- Compare branch: **feature/tu-feature**
- Título claro (ej. “Stage 5: Unified Output Renderer”)
- Descripción detallada:
  - Qué se agregó
  - Qué se mejoró
  - Qué módulos afecta
  - Screenshots si aplica

### Paso 5 — Revisión
Aunque seas tú solo, revisa tu propio PR como si fueras otra persona:

- ¿El código es claro?
- ¿Hay duplicación?
- ¿El renderer sigue consistente?
- ¿La UI se mantiene coherente?
- ¿El Makefile sigue funcionando?

### Paso 6 — Merge a main
Cuando todo esté listo:

- Merge → **Squash and merge** (recomendado)
- Esto mantiene el historial limpio.

### Paso 7 — Crear el release
Usa tu Makefile:

```bash
make release-patch
```

o

```bash
make release-minor
```

---

## 📦 6. Cómo preparar un release

1. Actualizar `CHANGELOG.md`
2. Crear rama de release:
   ```bash
   git checkout -b release/vX.Y.Z
   ```
3. Ajustar documentación si aplica
4. Merge a main
5. Crear tag con Makefile
6. Push del tag

---

## 🧪 7. Pruebas

Ejecutar pruebas:
```bash
pytest -q
```

Pruebas de estrés:
```bash
pytest tests/stress
```

---

## 📚 8. Guía de estilo del código

- Python: snake_case para funciones, PascalCase para clases.
- Módulos pequeños y enfocados.
- Evitar funciones mayores a 40 líneas.
- Documentar funciones públicas.
- Mantener consistencia en renderers y UIContract.

---

## 🤝 9. Reglas generales de contribución

- Mantener compatibilidad con tema claro/oscuro.
- No introducir dependencias innecesarias.
- No mezclar múltiples features en un solo PR.
- Mantener coherencia visual en todos los módulos.
- Mantener KEY_DISPATCH y renderer sincronizados.
- Mantener Makefile funcional en Windows y WSL.

---

## 🏁 10. Filosofía del proyecto

NA‑Engine busca ser:

- Modular  
- Extensible  
- Consistente  
- Elegante  
- Fácil de mantener  
- Profesional  

Cada contribución debe respetar estos principios.


---

