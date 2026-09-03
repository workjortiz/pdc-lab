# PROMPT_BASE — PDC App Framework
> Copia y pega este bloque a Claude al iniciar tu sesión de Vibe Coding en PDC Build.
> No lo modifiques — es el contrato técnico que mantiene tu app compatible con el framework.

---

Estoy desarrollando **PDC Lab** bajo el **PDC App Framework** de Grupo PDC.

**Nota especial:** esta app es pública — NO requiere login. Es el punto de entrada del framework, vive en su propio schema aislado `pdc_app_pdc_lab` (regla estándar, no es una excepción como PDC Registry).

**Stack obligatorio:** Python 3.11, Streamlit, SQLAlchemy ORM 2.0.
**BD local (desarrollo):** SQLite — archivo en `./data/app.db`.
**BD producción:** PostgreSQL (RDS), schema `pdc_app_pdc_lab`.

## Reglas que debes seguir siempre

1. **NUNCA escribas SQL crudo.** Siempre usa `session.query(Modelo)...` (SQLAlchemy ORM).
2. **SIEMPRE define longitud en columnas String** — `String(255)`, nunca `String` a secas.
3. **SIEMPRE usa `DateTime`** para fechas — nunca strings tipo `"2026-08-18"`.
4. **`Boolean`** se traduce automáticamente a `NUMBER(1)` en Oracle — no lo reemplaces por Integer.
5. **`app/auth.py` ya está implementado — no lo toques ni lo reimplementes.**
6. **`app/database.py` ya está configurado — impórtalo, no lo reescribas.**
7. Tus tablas van en `app/models.py`, heredando de `Base`.
8. El UI principal va en `app/main.py`.
9. **Naming:** tablas en singular y snake_case sin prefijo; columnas snake_case descriptivas.
10. **Nunca hardcodees credenciales.** Todo viene de `.env` (local) — en producción, del pipeline.
11. Aplica la línea gráfica PDC: Navy `#00216F` y Naranja `#FF5100` como colores protagonistas.
12. **Cuando modifiques un archivo, entrega SIEMPRE el archivo completo**, nunca un fragmento.
13. **Versionamiento semántico obligatorio.** Sube `version` en `pdc.config.json` (`MAYOR.MENOR.PARCHE`), agrega entrada en `CHANGELOG.md`, y muestra la versión en el sidebar (`v{version}`).
14. **Toda entrega de archivos va precedida de una tabla Archivo/Acción** (Reemplazar/Nuevo/Eliminar), sin excepción — incluso si es un solo archivo.
15. **El nombre del archivo entregado debe ser IDÉNTICO al nombre real del archivo del proyecto** — nunca sufijos como `main_pdc-lab.py`. El usuario arrastra el archivo completo para reemplazar; si se trabaja en varias apps a la vez, se separan en carpetas, nunca renombrando el archivo mismo.
16. **Cuando se entregue más de un archivo, empaquetarlos en un `.zip` nombrado `{NOMBRE_APP_MAYUSCULAS}_{version}.zip`** (ej. `PDC_LAB_1.1.1.zip`), archivos planos dentro, sin subcarpetas, nombres reales intactos.
17. **Toda sustitución de variables en un comando va acompañada de una tabla Variable/Valor**, en la app y en el chat — nunca implícita solo dentro del comando.
18. **Excepción — apps fundacionales (PDC Registry, PDC Lab):** schema vía Alembic incluso en local, no `create_all()`. Cada cambio a `models.py` trae su migración; el usuario corre `alembic upgrade head` antes de `streamlit run app/main.py`. **No aplica a apps normales de un PDC App Developer** — ahí el SQLite local sigue siendo sandbox desechable (`create_all()`), y la protección real ocurre sola en el pipeline de PDC Deploy.

## Cómo correrlo en local

```bash
pip install -r requirements.txt
streamlit run app/main.py
```
