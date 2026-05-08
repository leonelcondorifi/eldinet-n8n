# eldi

## Requisitos

- Python instalado

## Instalar dependencias en un venv

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicacion

```bash
uvicorn app.main:app --reload
```

## Ejecutar tests

```bash
pytest
```
