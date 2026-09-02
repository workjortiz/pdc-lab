# Changelog — PDC Lab

Formato: [MAYOR.MENOR.PARCHE] — fecha — qué cambió.

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
