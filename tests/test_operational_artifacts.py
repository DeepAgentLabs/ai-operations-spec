"""Draft operational schemas, safety boundaries and source-preserving projections."""
import copy
import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aios_reference import check, validator
from test_conformance_catalogs import normalize

ROOT = Path(__file__).parents[1]
V08 = ROOT / 'specification/v0.8'
CATALOG = json.loads((V08 / 'operational-rules.json').read_text())


def example(name):
    return json.loads((V08 / 'examples' / f'{name}.json').read_text())


@pytest.mark.parametrize('path', sorted((V08 / 'schemas').glob('*.schema.json')), ids=lambda p: p.name)
def test_schema_validity(path):
    Draft202012Validator.check_schema(json.loads(path.read_text()))


@pytest.mark.parametrize('path', sorted((V08 / 'examples').glob('*.json')), ids=lambda p: p.name)
def test_examples(path):
    assert check(json.loads(path.read_text())) == ('valid', [])


def test_catalog_and_conformance_text_agree_completely():
    document = normalize((V08 / 'conformance.md').read_text())
    quoted = []
    for rule in CATALOG['rules']:
        assert re.fullmatch(r'AIOS-0\.8-[RPCSD]\d{2}', rule['id'])
        assert rule['check'] in CATALOG['check_kinds']
        assert rule['role'] in {'producer', 'consumer', 'implementation'}
        assert rule['level'].split()[0] in rule['source_text']
        assert rule['source_text'] == rule['requirement']
        text = normalize(rule['source_text'])
        assert text in document
        quoted.append((document.index(text), document.index(text) + len(text)))
    for match in re.finditer(r'\b(MUST|SHOULD)\b', document):
        assert any(start <= match.start() < end for start, end in quoted)


@pytest.mark.parametrize('status', ['unavailable', 'error', 'skipped'])
def test_unavailable_assessment_cannot_be_a_pass_or_fake_confidence(status):
    doc = example('verification_unavailable')
    doc['status'] = status
    assert check(doc) == ('valid', [])
    for change in ({'verdict': 'supports'}, {'confidence': 0}, {'confidence': 1}):
        broken = {**doc, **change}
        assert check(broken) == ('schema-invalid', ['AIOS-0.8-R01'])


def test_unknown_safety_is_distinct_from_an_assessed_absence_of_concerns():
    doc = example('verification_signal')
    for status in ['no_concerns', 'not_checked']:
        doc['safety'] = {'status': status, 'concerns': []}
        assert check(doc) == ('valid', [])
    doc['safety'] = {'status': 'concerns', 'concerns': []}
    assert check(doc)[0] == 'schema-invalid'
    doc['safety']['concerns'].append('Synthetic unsafe instruction')
    assert check(doc) == ('valid', [])


def test_missing_measurements_are_not_invented():
    doc = example('verification_signal')
    doc.update(confidence=None, verdict='inconclusive')
    doc['grounding'].update(status='not_checked', unsupported_claims=[])
    assert check(doc) == ('valid', [])
    audit = example('audit_event')
    audit['actor'] = {'kind': 'unknown'}
    audit['outcome'] = 'unknown'
    assert check(audit) == ('valid', [])


def test_report_allows_hypotheses_and_separates_closure_from_recovery():
    doc = example('investigation_report')
    doc['summary'].update(certainty='hypothesis', evidence_ids=[])
    doc['findings'][0]['evidence_ids'] = []
    doc['incident'].update(status='resolved', native_state='dismissed')
    doc['recovery'] = {'status': 'not_attempted', 'evidence_ids': []}
    assert check(doc) == ('valid', [])
    doc['recovery']['status'] = 'verified'
    assert check(doc) == ('semantic-invalid', ['AIOS-0.8-R06'])
    doc['recovery']['evidence_ids'] = ['lens-run']
    assert check(doc) == ('valid', [])


def test_schema_registry_keeps_both_common_schema_identities_offline():
    doc = example('audit_event')
    doc['extensions'] = {'org.example.audit': {'future': {'opaque': [1, 2]}}}
    original = copy.deepcopy(doc)
    validator(doc).validate(doc)
    assert check(doc) == ('valid', [])
    assert doc == original
    doc['extensions'] = {'aiops.private': {}}
    assert check(doc)[0] == 'schema-invalid'


def test_time_comparison_uses_timezone_instants():
    doc = example('audit_event')
    doc['occurred_at'] = '2026-11-04T12:04:00-06:00'
    assert check(doc) == ('valid', [])
    doc['occurred_at'] = '2026-11-04T13:04:00-06:00'
    assert check(doc) == ('semantic-invalid', ['AIOS-0.8-R04'])


@pytest.mark.parametrize('field', ['summary', 'recovery'])
def test_observed_and_verified_claims_need_a_declared_citation(field):
    doc = example('investigation_report')
    doc[field]['evidence_ids'] = ['not-declared']
    if field == 'recovery':
        doc[field]['status'] = 'verified'
    assert check(doc) == ('semantic-invalid', ['AIOS-0.8-R03', 'AIOS-0.8-R06'])


def test_timestamp_designator_case_does_not_change_the_instant():
    doc = example('audit_event')
    doc['occurred_at'] = doc['occurred_at'].lower()
    doc['created_at'] = doc['created_at'].lower()
    assert check(doc) == ('valid', [])


def test_catalog_applicability_matches_semantic_rule_domains():
    expected = {
        'R02': ['verification_signal', 'investigation_report'],
        'R03': ['investigation_report'],
        'R04': ['audit_event', 'investigation_report'],
        'R05': ['verification_signal'],
        'R06': ['investigation_report'],
        'R07': ['audit_event'],
    }
    for rule in CATALOG['rules']:
        if rule['check'] == 'semantic':
            assert rule['applies_to'] == expected[rule['id'].split('-')[-1]]


@pytest.mark.parametrize('secret_field', ['credentials', 'credential_hash', 'arguments', 'execution_context'])
def test_closed_envelopes_reject_raw_privileged_fields(secret_field):
    for kind in ['audit_event', 'verification_signal', 'investigation_report']:
        doc = example(kind)
        doc[secret_field] = 'synthetic secret'
        assert check(doc) == ('schema-invalid', ['AIOS-0.8-R01'])
