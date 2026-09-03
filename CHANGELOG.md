# Changelog — PDC Lab

Formato: [MAYOR.MENOR.PARCHE] — fecha — qué cambió.

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
