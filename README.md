# Biblioteca Digital

Sistema web para la gestión integral de una biblioteca: libros, autores, socios y préstamos.

## Tecnologías
- Python 3 + Flask
- SQLite (sin ORM)
- HTML + CSS (Jinja2)
- Arquitectura MVC + Patrón Repository

## Estructura
```
biblioteca_web/
  app.py, config.py, database.py, run.py
  models/        → entidades de dominio
  repositories/  → acceso a datos
  controllers/   → blueprints Flask
  views/         → templates HTML
  static/css/    → estilos
```

## Instalación
```bash
pip install -r requirements.txt
python biblioteca_web/run.py
```

## Recursos
- Tablero Trello: https://trello.com/b/FanPtJxV/biblioteca-digital-lenguajes-de-programacion
- Materia: Lenguajes de Programación
- Autor: Johan Steven Potosi Jurado
