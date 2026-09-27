"""Frozen UI choice benchmark with abstention and Brier score."""
import json
import sys
from pathlib import Path


def check(cases, predictions):
    by_id = {p['case_id']: p for p in predictions}
    if len(by_id) != len(predictions) or set(by_id) != {c['id'] for c in cases}:
        raise ValueError('predictions must cover every unique case exactly once')
    details = []
    for case in cases:
        pred = by_id[case['id']]
        ids = {a['id'] for a in case['actions']}
        choice = pred['choice']
        if choice is not None and choice not in ids:
            raise ValueError(f'unknown action {choice}')
        confidence = pred['confidence']
        if not 0 <= confidence <= 1:
            raise ValueError('confidence must be in [0,1]')
        correct = choice in case['acceptable']
        # Confidence is confidence in the submitted choice, including abstention.
        brier = (confidence - int(correct)) ** 2
        details.append({'case_id': case['id'], 'correct': correct, 'abstained': choice is None, 'brier': round(brier, 4)})
    return {'ok': all(d['correct'] for d in details), 'accuracy': round(sum(d['correct'] for d in details) / len(details), 4),
            'mean_brier': round(sum(d['brier'] for d in details) / len(details), 4), 'cases': details}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('demo', 'check'):
        raise SystemExit('usage: tool.py demo | check CASES.json PREDICTIONS.json')
    base = Path(__file__).parent / 'examples'
    cases = json.loads((base / 'cases.json').read_text()) if sys.argv[1] == 'demo' else json.loads(Path(sys.argv[2]).read_text())
    predictions = json.loads((base / 'predictions.json').read_text()) if sys.argv[1] == 'demo' else json.loads(Path(sys.argv[3]).read_text())
    result = check(cases, predictions)
    print(json.dumps(result, indent=2))
    return 0 if sys.argv[1] == 'demo' or result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
