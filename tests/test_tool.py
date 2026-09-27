import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tool import check, import_clm_rank
ROOT = Path(__file__).resolve().parents[1] / 'examples'
CASES = json.loads((ROOT / 'cases.json').read_text())
PRED = json.loads((ROOT / 'predictions.json').read_text())
CLM = json.loads((ROOT / 'clm-rank-responses.json').read_text())

class ChoiceTests(unittest.TestCase):
    def test_wrong_scope_is_counted(self):
        result = check(CASES, PRED)
        self.assertEqual(result['accuracy'], 0.5)
        self.assertFalse(result['ok'])

    def test_correct_action_passes(self):
        pred = copy.deepcopy(PRED)
        pred[0]['choice'] = 'own'
        self.assertTrue(check(CASES, pred)['ok'])

    def test_invalid_choice_rejected(self):
        pred = copy.deepcopy(PRED)
        pred[0]['choice'] = 'not-in-state'
        with self.assertRaises(ValueError):
            check(CASES, pred)

    def test_clm_import_maps_duplicate_labels_by_scope(self):
        predictions = import_clm_rank(CASES, CLM)
        self.assertEqual(predictions[0]['choice'], 'shared')
        self.assertIsNone(predictions[1]['choice'])

    def test_clm_import_rejects_missing_candidate(self):
        responses = copy.deepcopy(CLM)
        responses[0]['ranked'].pop()
        with self.assertRaises(ValueError):
            import_clm_rank(CASES, responses)

    def test_clm_import_rejects_duplicate_rank(self):
        responses = copy.deepcopy(CLM)
        responses[0]['ranked'][1]['rank'] = 1
        with self.assertRaises(ValueError):
            import_clm_rank(CASES, responses)
