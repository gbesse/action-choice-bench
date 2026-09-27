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
        confidence = pred.get('confidence')
        if confidence is not None and not 0 <= confidence <= 1:
            raise ValueError('confidence must be in [0,1]')
        correct = choice in case['acceptable']
        # A ranking softmax is not calibrated correctness confidence.
        brier = (confidence - int(correct)) ** 2 if confidence is not None else None
        details.append({'case_id': case['id'], 'correct': correct, 'abstained': choice is None,
                        'brier': round(brier, 4) if brier is not None else None})
    scored = [d['brier'] for d in details if d['brier'] is not None]
    return {'ok': all(d['correct'] for d in details), 'accuracy': round(sum(d['correct'] for d in details) / len(details), 4),
            'mean_brier': round(sum(scored) / len(scored), 4) if scored else None,
            'brier_samples': len(scored), 'cases': details}


def candidate_text(action):
    return action.get('candidate_text') or f'{action["label"]} [{action["scope"]}]'


def import_clm_rank(cases, responses, abstain_below=0.6):
    """Map recorded CLM /v1/rank responses to semantic action IDs."""
    if not 0 <= abstain_below <= 1:
        raise ValueError('abstention threshold must be in [0,1]')
    by_id = {response['case_id']: response for response in responses}
    if len(by_id) != len(responses) or set(by_id) != {case['id'] for case in cases}:
        raise ValueError('one CLM response is required for each case')
    predictions = []
    for case in cases:
        lookup = {candidate_text(action): action['id'] for action in case['actions']}
        if len(lookup) != len(case['actions']):
            raise ValueError(f'{case["id"]}: candidate texts must be unique')
        ranked = by_id[case['id']]['ranked']
        if {item['candidate'] for item in ranked} != set(lookup) or len(ranked) != len(lookup):
            raise ValueError(f'{case["id"]}: ranked candidates do not match actions')
        if {item['rank'] for item in ranked} != set(range(1, len(ranked) + 1)):
            raise ValueError(f'{case["id"]}: ranks must be unique and contiguous')
        if any(not 0 <= item['prob'] <= 1 for item in ranked):
            raise ValueError(f'{case["id"]}: probabilities must be in [0,1]')
        winner = min(ranked, key=lambda item: item['rank'])
        probability = winner['prob']
        predictions.append({'case_id': case['id'],
                            'choice': lookup[winner['candidate']] if probability >= abstain_below else None,
                            'confidence': None, 'rank_probability': probability})
    return predictions


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('demo', 'check', 'clm-demo', 'import-clm'):
        raise SystemExit('usage: tool.py demo | check CASES.json PREDICTIONS.json | clm-demo | import-clm CASES.json RESPONSES.json [THRESHOLD]')
    base = Path(__file__).parent / 'examples'
    if sys.argv[1] in ('clm-demo', 'import-clm'):
        cases = json.loads((base / 'cases.json').read_text()) if sys.argv[1] == 'clm-demo' else json.loads(Path(sys.argv[2]).read_text())
        responses = json.loads((base / 'clm-rank-responses.json').read_text()) if sys.argv[1] == 'clm-demo' else json.loads(Path(sys.argv[3]).read_text())
        threshold = 0.6 if sys.argv[1] == 'clm-demo' or len(sys.argv) < 5 else float(sys.argv[4])
        predictions = import_clm_rank(cases, responses, threshold)
        result = {'predictions': predictions, 'benchmark': check(cases, predictions)} if sys.argv[1] == 'clm-demo' else predictions
        print(json.dumps(result, indent=2))
        return 0
    cases = json.loads((base / 'cases.json').read_text()) if sys.argv[1] == 'demo' else json.loads(Path(sys.argv[2]).read_text())
    predictions = json.loads((base / 'predictions.json').read_text()) if sys.argv[1] == 'demo' else json.loads(Path(sys.argv[3]).read_text())
    result = check(cases, predictions)
    print(json.dumps(result, indent=2))
    return 0 if sys.argv[1] == 'demo' or result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
