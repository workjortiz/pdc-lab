# PDC Lab

App pública de intake del **PDC App Framework** — punto de entrada, sin login. Cualquier persona con el link puede registrar una idea, sin necesidad de tener nada instalado todavía.

## Por qué esta app existe (y por qué es pública)

Antes de esta app, "PDC Lab" era solo un canvas conversacional (SPEC §3). El problema: para llenar cualquier formulario técnico, el usuario necesitaría VS Code + Git + Python — pero **PDC Lab es precisamente donde se detecta si le falta alguna de esas herramientas**. Solución: esta app vive ya desplegada (su propio EC2 + Nginx, como PDC Registry), accesible solo con navegador — cero dependencias del lado del usuario.

## El puente hacia PDC Registry — por qué es un correo, no una lectura de BD

`pdc-lab` vive en su propio schema aislado (`pdc_app_pdc_lab`), siguiendo la regla estándar del framework (no es una excepción como PDC Registry). Por la regla de oro de aislamiento (SPEC §4.4), **PDC Registry no puede leer directamente el schema de `pdc-lab`**. El puente es el correo tipo ticket (vía Power Automate, mismo patrón que las notificaciones de Teams del pipeline): IT recibe la solicitud, la revisa en la cola interna de `pdc-lab`, y una vez aprobada, **crea la entrada correspondiente en PDC Registry manualmente** — igual que ya se hace con el manifiesto de infraestructura.

## Modelo de datos

Una sola tabla, `Solicitud`, con 4 bloques:
- **Identidad:** nombre, correo, empresa/mundo, división, país — pre-llena los tags de AWS que usará IT después
- **Diagnóstico técnico:** sistema operativo, si la laptop es gestionada por IT, si ya tiene VS Code/Git/Python
- **Canvas de PDC Lab:** nombre de app propuesto, descripción del problema
- **Workflow:** estado (Pendiente/Revisada/Aprobada/Rechazada), notas de IT

## Cómo correrlo en local

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

Dos vistas dentro de la misma app (selector arriba):
- **📝 Registrar una idea** — el formulario público
- **🔐 Acceso IT** — la cola de solicitudes, pide la clave de `ADMIN_ACCESS_CODE` en `.env`

## Notificación por correo (Power Automate)

Configura `POWER_AUTOMATE_WEBHOOK_URL` en `.env` con la URL del flow de Teams/Power Automate que arma y envía el correo al distribution list de Integraciones Digitales. Si queda vacío, la app sigue funcionando normal — solo se omite la notificación (el registro en base de datos no depende del correo).

---
*Grupo PDC — División de Integraciones Digitales*
