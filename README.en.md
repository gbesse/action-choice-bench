# action-choice-bench

Measures action selection and abstention on frozen UI states.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Related projects

- [CLM — contrastive action ranking](https://github.com/Contrastive-LM/CLM)
- [Jev GUI Delegate — UI decision delegation](https://github.com/YUTA-fywoo/jev-gui-delegate)
- [Jevry — bounded UI decisions](https://github.com/michaelswissa/jevry)

These projects document the need or cover part of the problem. No affiliation or integration with them is claimed.

## Quick start

```bash
python3 tool.py demo
python3 tool.py check examples/cases.json examples/predictions.json
```

Python 3.11+; no external package required. / Python 3.11+ ; aucune dépendance externe. / Python 3.11+; sin dependencias externas.

## Current scope

Two synthetic UI states and JSON predictions illustrate the format, accuracy, abstention and Brier score. This tiny set does not yet predict full browser-agent success.

## CLM-related demo

The importer accepts recorded responses in [CLM's `POST /v1/rank` format](https://github.com/Contrastive-LM/CLM#api-reference), wrapped with `case_id`. It maps each candidate text to a unique action ID and can abstain below a threshold:

```bash
python3 tool.py clm-demo
python3 tool.py import-clm examples/cases.json examples/clm-rank-responses.json > predictions.json
```

The bundled responses are synthetic; no CLM model runs. A CLM ranking probability is not treated as calibrated correctness confidence, so the Brier score is `null` for this import.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT.
