"""Canonical artifact outcomes, including extension/core separation."""
import copy
import json
from pathlib import Path

import pytest

from test_v04_schema import semantic_errors, validator

EXAMPLES = Path(__file__).parents[1] / 'specification' / 'v0.6' / 'examples'
MANIFEST = json.loads((EXAMPLES / 'manifest.json').read_text())


@pytest.mark.parametrize('case', MANIFEST['cases'], ids=lambda case: case['path'])
def test_canonical_outcomes(case: dict) -> None:
    artifact = json.loads((EXAMPLES / case['path']).read_text())
    assert artifact['spec_version'] == MANIFEST['spec_version']
    structural = list(validator(artifact).iter_errors(artifact))
    if case['expected'] == 'schema-invalid':
        assert structural
    else:
        assert not structural
        assert bool(semantic_errors(artifact)) == (case['expected'] == 'semantic-invalid')


def test_manifest_covers_every_artifact_once() -> None:
    paths = [case['path'] for case in MANIFEST['cases']]
    assert len(paths) == len(set(paths))
    assert set(paths) == {path.name for path in EXAMPLES.glob('*.json')} - {'manifest.json'}
    assert {case['expected'] for case in MANIFEST['cases']} == {
        'valid', 'schema-invalid', 'semantic-invalid',
    }


@pytest.mark.parametrize('payload', [None, [], {'version': '99.0', 'future': [None, {'a': True}]}])
def test_unknown_extension_payload_does_not_change_core_alignment(payload: object) -> None:
    artifact = json.loads((EXAMPLES / 'advanced-support-run.json').read_text())
    artifact['extensions']['org.example.support'] = payload
    validator(artifact).validate(artifact)
    assert not semantic_errors(artifact)
    core = copy.deepcopy(artifact)
    del core['extensions']
    core['events'] = [event for event in core['events'] if event['event_name'].startswith('aiops.')]
    validator(core).validate(core)
    assert not semantic_errors(core)


def test_valid_extension_cannot_rescue_invalid_core() -> None:
    artifact = json.loads((EXAMPLES / 'advanced-support-run.json').read_text())
    artifact['custom_top_level'] = {'org.example.support': {}}
    assert list(validator(artifact).iter_errors(artifact))
    del artifact['custom_top_level']
    artifact['relationships'][0]['target'].pop('external')
    validator(artifact).validate(artifact)
    assert semantic_errors(artifact)
