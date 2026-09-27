# action-choice-bench

Mide la selección de acciones y la abstención en estados de interfaz fijos.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Proyectos relacionados

- [CLM — clasificación contrastiva de acciones](https://github.com/Contrastive-LM/CLM)
- [Jev GUI Delegate — delegación de decisiones de interfaz](https://github.com/YUTA-fywoo/jev-gui-delegate)
- [Jevry — decisiones de interfaz acotadas](https://github.com/michaelswissa/jevry)

Estos proyectos documentan la necesidad o cubren parte del problema. No se afirma ninguna afiliación ni integración con ellos.

## Inicio rápido

```bash
python3 tool.py demo
python3 tool.py check examples/cases.json examples/predictions.json
```

Python 3.11+; no external package required. / Python 3.11+ ; aucune dépendance externe. / Python 3.11+; sin dependencias externas.

## Alcance actual

Dos estados de interfaz sintéticos y predicciones JSON ilustran el formato, la exactitud, la abstención y la puntuación de Brier. Este conjunto mínimo todavía no predice el éxito de un agente de navegador completo.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

## Licencia

MIT.
