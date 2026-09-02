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

## Cómo correrlo en local

```bash
pip install -r requirements.txt
streamlit run app/main.py
```
