# Operational artifact examples

All examples are synthetic projections of inspected implementation shapes,
not emitted output from a shipped sibling exporter. Native source mappings and
limitations are recorded in [the evidence notes](../../reviews/operational-artifact-mappings.md).

| Example | Expected result | Purpose |
| --- | --- | --- |
| [Completed verification](examples/verification_signal.json) | valid | Partial support, measured confidence and unassessed safety |
| [Unavailable verification](examples/verification_unavailable.json) | valid | No verdict or invented confidence |
| [Audit denial](examples/audit_event.json) | valid | A denied attempted dispatch, preserving correlation |
| [Investigation](examples/investigation_report.json) | valid | Observed failure, hypothetical cause, pending recovery |

The [portable conformance suite](../v0.6/conformance-suite/README.md) adds
negative controls for unavailable-as-pass, privacy wrapper fields, timestamp
ordering, duplicate identities, missing grounding, undeclared citations,
unsupported markers and recovery without evidence.

From the repository root:

```bash
uv sync --extra dev
uv run pytest tests/test_operational_artifacts.py tests/test_v06_conformance_suite.py
make docs
```

These are offline reference checks. Reference presence does not authenticate a
producer or fetch source content; consumers need their own explicitly configured
source readers. Run and Workflow remain 0.4-draft, provenance remains 0.6-draft.
