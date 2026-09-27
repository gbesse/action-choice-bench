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

## Demo relacionada con CLM

El importador acepta respuestas guardadas con el formato [`POST /v1/rank` de CLM](https://github.com/Contrastive-LM/CLM#api-reference), envueltas con `case_id`. Asocia cada texto candidato con un ID de acción único y puede abstenerse por debajo de un umbral:

```bash
python3 tool.py clm-demo
python3 tool.py import-clm examples/cases.json examples/clm-rank-responses.json > predictions.json
```

Las respuestas incluidas son sintéticas; no se ejecuta ningún modelo CLM. Una probabilidad de clasificación de CLM no se trata como confianza calibrada de acierto; la puntuación de Brier queda en `null` para esta importación.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

## Licencia

MIT.
