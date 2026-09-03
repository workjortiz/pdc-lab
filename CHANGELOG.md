# Changelog — PDC Lab

Formato: [MAYOR.MENOR.PARCHE] — fecha — qué cambió.

---

## [2.3.0] — 2026-09-03

- Nuevo: el JSON exportado (formulario y cola de IT) ahora incluye `nombre_colaborador` (tomado de "Nombre completo") — permite que PDC Registry autocomplete el nombre del colaborador nuevo, sin volver a teclearlo
- Quitado del JSON: `usuarios_adicionales`, `github_repo_url`, `url_produccion` — esos campos ya no se piden en el registro inicial de PDC Registry (se completan después, en Aprovisionamiento)

---

## [2.2.1] — 2026-09-03

- Fix: `NameError: name 'datetime' is not defined` al enviar el formulario — faltaba `from datetime import datetime` en `main.py` (la usaba `construir_nombre_archivo()`, agregada en v1.4.1, pero solo se probó de forma aislada, no dentro del archivo real)
- Fix: si la generación del JSON/nombre de archivo falla por cualquier razón, ya no tumba toda la pantalla — la solicitud queda guardada igual (eso ocurre antes) y se muestra un aviso en vez de un error

---

## [2.2.0] — 2026-09-02

- Fix: "Código colaborador" ahora es un campo numérico real (`number_input`) — ya no permite escribir letras en absoluto, no solo rechazarlas al enviar
- Fix: "Nombre completo", "Correo corporativo" y "División / Área" ahora se ven en MAYÚSCULAS de inmediato al tabular fuera del campo — se movieron fuera del formulario porque Streamlit no reacciona en vivo a cambios dentro de un `st.form` (solo al enviar)
- Cambio: etiqueta "¿Tienes Git?" → "¿Tienes un Gestor Git?"

---

## [2.1.0] — 2026-09-02

- Cambio: "Código colaborador (RRHH)" pasa de opcional a **obligatorio**, y se valida que sea solo numérico
- Fix: "Correo corporativo" y "División / Área" ahora también se guardan y exportan en MAYÚSCULAS (antes solo aplicaba a "Nombre completo")

---

## [2.0.1] — 2026-09-02

- Aclaración en `PROMPT_BASE.md`: Alembic-en-local es excepción de apps fundacionales, no norma general — mismo cambio que PDC Registry.

---

## [2.0.0] — 2026-09-02

- **Cambio de arquitectura:** el schema local ahora se gestiona con Alembic, no con `init_db()`/`create_all()` — mismo motivo y mecanismo que PDC Registry.
- Agregada la carpeta `migrations/` completa.
- **Migración única, una sola vez:**
  ```bash
  alembic stamp 0001
  alembic upgrade head
  ```

---

## [1.5.0] — 2026-09-02

- Nuevo: campo opcional "¿Ya tienes código colaborador? (RRHH)" en el formulario público
- El JSON exportado (formulario y cola de IT) ahora incluye `codigo_colaborador`, para que PDC Registry pueda vincular la app al colaborador correcto automáticamente

---

## [1.4.1] — 2026-09-02

- Fix: nombre de archivo del JSON descargado ahora es `Registro_{fecha}_{AUTOR}_{APP}.json` (ej. `Registro_20260902_JUANORTIZ_PDCLAB.json`), en vez del genérico `{nombre}-registro.json` — más fácil de identificar entre varias descargas

---

## [1.4.0] — 2026-09-02

- Nuevo: pantalla de cierre separada ("✅ Formulario Concluido") tras enviar la solicitud — ya no convive con el formulario, evita la duda de "¿esto se guardó o no?". Botón "Registrar otra idea" para volver a empezar.
- Fix: "Nombre completo" se guarda y exporta siempre en MAYÚSCULAS, sin importar cómo se haya digitado
- Cambio: opciones del dropdown "Empresa / mundo" actualizadas a NEXO, VIKINGO DISTRIBUIDORA, PDC BRANDS, MOSTRO

---

## [1.3.0] — 2026-09-02

- Cambio de diseño: el botón del formulario público ahora dice **"Solicitar Registro"** y, al guardar la solicitud, genera al instante un JSON listo para importar en PDC Registry — sin pasar por ninguna vista de IT
- Quitado: la sección "📇 Auto-registro en PDC Registry" de Acceso IT — era un atajo de bootstrap útil solo para registrar `pdc-lab` misma (nació antes de que este proceso existiera), no una feature permanente
- Refactor: la lógica de mapeo a formato PDC Registry ahora vive en una sola función (`construir_registro_json`), reutilizada tanto en el formulario público como en el botón de exportar de la cola de IT

---

## [1.2.0] — 2026-09-02

- Nuevo: sección "📇 Auto-registro en PDC Registry" en la vista de IT — genera el JSON de la propia app (leyendo su `pdc.config.json`) listo para importar en PDC Registry, sin escribirlo a mano
- `pdc.config.json` ampliado con los campos que este export necesita: `descripcion`, `estado`, `ambiente`, `github_repo_url`, `url_produccion`, `usuarios_adicionales`

---

## [1.1.1] — 2026-09-02

- Fix: agregado el badge de versión visible (`vX.Y.Z`) bajo el título — esta app no tiene sidebar como PDC Registry, así que antes no había forma de confirmar si un cambio se aplicó correctamente

---

## [1.1.0] — 2026-09-02

- Nuevo: botón "Exportar como JSON" en cada solicitud de la vista de IT — genera un archivo compatible con el importador de PDC Registry, cerrando el ciclo sin retecleo manual

---

## [1.0.0] — 2026-09-02

Versión inicial de PDC Lab.

- Formulario público de intake (sin login): identidad, diagnóstico técnico, canvas de PDC Lab
- Notificación tipo ticket vía webhook de Power Automate (best-effort, no bloquea el guardado)
- Vista de IT con gate por clave compartida: cola de solicitudes, edición de estado y notas
- Modelo de datos: `Solicitud`, schema aislado `pdc_app_pdc_lab`

**Pendiente:** esta app usa `layout="centered"` sin sidebar — el badge de versión todavía no tiene un lugar visual definido aquí (a diferencia de PDC Registry). Resolver cuando se retome el calibrado de esta app.
