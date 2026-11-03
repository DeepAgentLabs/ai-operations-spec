"""Validate the companion catalog and paired example without an OTel SDK."""
import json
import re
from datetime import datetime
from pathlib import Path

from test_v04_schema import semantic_errors, validator

ROOT = Path(__file__).parents[1]
OTEL = ROOT / 'specification/v0.6/otel'


def test_mapping_covers_each_canonical_event_once():
    catalog = json.loads((OTEL / 'mapping.json').read_text())
    common = json.loads((ROOT / 'specification/v0.4/schemas/common.schema.json').read_text())
    names = [row['event_name'] for row in catalog['events']]
    assert len(names) == len(set(names))
    assert set(names) == set(common['$defs']['canonical_event_name']['enum'])
    for row in catalog['events']:
        assert row['carrier'] == 'span_event_or_log'
        assert set(row['preserve']) == {
            'event_id', 'event_name', 'occurred_at', 'object_id', 'object_type',
        }
    assert catalog['upstream_semconv'] == '1.37.0'
    assert catalog['profile'] == 'aios.otel/1'


def test_retry_projection_preserves_observations_and_units():
    example = json.loads((OTEL / 'example.json').read_text())
    run = example['artifact']
    validator(run).validate(run)
    assert not semantic_errors(run)
    spans = example['projection']['spans']
    assert len(spans) == len(run['occurrences']) == 2
    assert len({span['span_id'] for span in spans}) == 2
    native = {event['event_id']: event for event in run['events']}
    projected_ids = []
    for span, occurrence in zip(spans, run['occurrences']):
        assert re.fullmatch('[0-9a-f]{32}', span['trace_id'])
        assert re.fullmatch('[0-9a-f]{16}', span['span_id'])
        assert span['attributes']['aios.object_id'] == occurrence['id']
        assert span['attributes']['aios.run_id'] == run['id']
        start = datetime.fromisoformat(span['start_time'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(span['end_time'].replace('Z', '+00:00'))
        duration = occurrence['attributes']['duration']
        assert duration['unit'] == 'ms'
        assert duration['kind'] == 'observed'
        duration_ms = duration['value']
        assert (end - start).total_seconds() * 1_000_000_000 == span['duration_ns']
        assert span['duration_ns'] == duration_ms * 1_000_000
        for event in span['events']:
            eid = event['attributes']['aios.event_id']
            projected_ids.append(eid)
            source = native[eid]
            assert event['name'] == source['event_name']
            assert event['timestamp'] == source['occurred_at']
            assert event['attributes']['aios.object_id'] == source['object_id']
            assert event['attributes']['aios.object_type'] == source['object_type']
            if 'outcome' in source['attributes']:
                assert event['attributes']['outcome'] == source['attributes']['outcome']
    assert len(projected_ids) == len(set(projected_ids))
    assert set(projected_ids) == set(native)
    assert spans[0]['status'] == 'ERROR'
    assert spans[1]['status'] == 'UNSET'
    assert run['status'] == 'completed'
    assert [o['status'] for o in run['occurrences']] == ['failed', 'completed']
