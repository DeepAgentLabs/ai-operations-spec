# v0.6 Draft Extension Model

## Status and scope

Exploratory draft, dependent on v0.1–v0.5. This document elaborates the existing
v0.4 open extension points; it does not alter their schemas. Requirements apply
within this draft. See [v0.4 conformance](../v0.4/conformance.md) and
[v0.5 compatibility](../v0.5/versioning.md).

## Placement and naming

A producer MUST use an existing core field when its defined meaning matches.
Producer-specific metadata MAY use `attributes` where the selected object schema
permits it. An `attributes` key has no shared semantics merely because two
producers spell it the same way. Structured contracts intended for third-party
reuse SHOULD use `extensions` where the selected schema permits it.

An extension key MUST match the v0.4 `extension_name` grammar: at least three
lowercase dot-separated segments, each containing lowercase ASCII letters or
digits with optional internal hyphens or underscores. The `aiops` namespace is
reserved and MUST NOT be used for producer-defined extensions or events.
For example, `org.example.support` is legal; `support`, `Org.Example.Support`
and `aiops.support.extra` are not. Producers SHOULD use a domain they control,
reverse its labels and append a meaningful component. Syntax validation does
not verify domain ownership. `org.example` is illustrative, not a namespace
that implementers should adopt in production.

An extension event MUST use the same reverse-domain grammar and target an
existing permitted object type. Extensions MUST NOT add members to closed
object, reference, relationship or evidence vocabularies. New core fields are
not extension points: an unknown top-level field remains schema-invalid.

## Meaning and preservation

An extension MUST NOT redefine core fields, weaken core invariants or make an
otherwise invalid artifact valid. Core interpretation MUST remain possible
without understanding an extension. Consumers MUST preserve unknown attributes
and namespaced extension entries, including nested values, arrays and nulls,
when reading and re-emitting the same artifact. Preservation means JSON-value
equality; whitespace and member order need not survive. Consumers MUST NOT
execute code or fetch URLs merely because an extension contains them.

Core draft alignment does not certify extension payload validity. A consumer
MAY separately validate an understood extension against its publisher's schema;
it SHOULD report extension-contract failures separately from core failures.
A valid core artifact can contain an unsupported extension version. A consumer
that requires that extension for a specific operation SHOULD decline that
operation explicitly instead of guessing semantics or rejecting core alignment.
Unknown extension events are preserved but do not imply canonical event meaning.

## Publishing a reusable extension

A publisher SHOULD publish a contract containing:

- namespace and owner/contact, purpose and applicable host objects;
- payload schema or precise shape, realistic example and negative example;
- version marker and explicit unknown-version handling;
- compatibility, deprecation and migration policy;
- privacy guidance and interpretation limits, including any external references.

The core schema imposes no payload shape or extension version field. A publisher
MAY define its own payload `version` as illustrated in the canonical examples;
that value versions only that extension, never `spec_version`. A breaking payload
change SHOULD use a distinct major version or namespace with documented routing.
Consumers MUST NOT infer compatibility from a namespace alone. Extension
publication does not register a new normative AIOS concept. Shared concepts
require an ordinary specification proposal and the applicable review gates.

## Privacy and external references

Examples use synthetic values. Publishers SHOULD minimize personal data and
secrets and document redaction behavior. An extension URL is opaque producer
metadata; it is not a resolved AIOS relationship. Core external endpoints still
require `external: true`, and consumers MUST NOT claim verified resolution unless
they actually resolve them. Extension values cannot grant authority to execute
an action, approve a release or bypass supervision.
