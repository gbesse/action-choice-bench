# action-choice-bench

Mesure les choix d’action et l’abstention sur des états UI figés.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Projets voisins

- [CLM — classement contrastif des actions](https://github.com/Contrastive-LM/CLM)
- [Jev GUI Delegate — délégation de décisions UI](https://github.com/YUTA-fywoo/jev-gui-delegate)
- [Jevry — agent UI à décisions bornées](https://github.com/michaelswissa/jevry)

Ces projets documentent le besoin ou couvrent une partie du problème. Aucun lien d’affiliation ni intégration avec eux n’est revendiqué.

## Démarrer

```bash
python3 tool.py demo
python3 tool.py check examples/cases.json examples/predictions.json
```

Python 3.11+; no external package required. / Python 3.11+ ; aucune dépendance externe. / Python 3.11+; sin dependencias externas.

## Portée actuelle

Deux états UI synthétiques et des prédictions JSON illustrent le format, la précision, l’abstention et le score de Brier. Ce jeu minimal ne prédit pas encore la réussite d’un agent navigateur complet.

## Démo liée à CLM

L’importeur accepte des réponses enregistrées au format [`POST /v1/rank` de CLM](https://github.com/Contrastive-LM/CLM#api-reference), enveloppées avec `case_id`. Il mappe chaque texte candidat à un identifiant d’action unique et peut s’abstenir sous un seuil :

```bash
python3 tool.py clm-demo
python3 tool.py import-clm examples/cases.json examples/clm-rank-responses.json > predictions.json
```

Les réponses fournies sont synthétiques ; aucun modèle CLM n’est exécuté. Une probabilité de classement CLM n’est pas traitée comme une confiance calibrée de justesse : le score de Brier reste `null` pour cet import.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Licence

MIT.
