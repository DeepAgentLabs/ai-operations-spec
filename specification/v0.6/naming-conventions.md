# v0.6 Draft Naming Conventions

## Status and scope

Exploratory draft, dependent on v0.1–v0.5. This document records the naming
rules the v0.4 schemas already follow and makes them binding for every new
core field, schema, closed-vocabulary member and catalog the specification
publishes. It renames nothing: every existing v0.4 name already complies, and
`tests/test_naming_conventions.py` fails if a schema drifts from these rules.

The rules govern names defined by the specification. Keys inside freeform
`attributes` objects and inside namespaced `extensions` payloads belong to
their producer or extension publisher; they SHOULD follow the same rules for
readability, but a consumer MUST NOT reject an artifact because they do not.

## Field names

A specification-defined field name MUST match `^[a-z][a-z0-9]*(_[a-z0-9]+)*$`:
lowercase ASCII `snake_case`, starting with a letter, with no leading,
trailing or doubled underscores. Field names are English words, not
abbreviations (see "Abbreviations" below).

| Pattern | Meaning | Examples |
|---|---|---|
| `id` | The identity of the object that holds it | `id` |
| `<noun>_id` | The identity of a different object being referenced | `workflow_id`, `object_id`, `event_id` |
| `<noun>_type` | A discriminator drawn from a closed vocabulary | `artifact_type`, `object_type` |
| `<noun>_name` | A name drawn from a catalog or grammar | `event_name` |
| `<past participle>_at` | An RFC 3339 `date-time` instant | `started_at`, `ended_at`, `occurred_at` |
| `<noun>_version` | A version marker | `spec_version` |

A field ending in `_at` MUST be a `date-time` value, and a `date-time` value
MUST use a field ending in `_at`. A field ending in `_id` MUST hold an
identifier. Durations and other quantities MUST NOT use the `_at` suffix;
they belong in `measurements` with an explicit `unit`.

## Singular and plural

A field whose value is a JSON array MUST be a plural noun (`steps`,
`relationships`, `measurements`). An open-keyed map whose members are
independent entries is also plural (`attributes`, `extensions`). Every other
field MUST be singular (`source`, `target`, `status`).

Mass nouns that have no plural MAY name an array and MUST be listed here:
`evidence` and `lineage`. Adding a mass noun to this list is a change to this
document, not a producer decision.

## Booleans

A boolean field MUST be an adjective or past participle that reads as true
when set (`external`, `frozen`). It MUST NOT use an `is_` or `has_` prefix
and MUST NOT be phrased negatively (`unresolved`, `not_external`).

## Vocabulary values

Closed-vocabulary members are lowercase ASCII and never change spelling once
published (decision `D-004`; see [v0.4 conformance](../v0.4/conformance.md)).

| Vocabulary | Form | Examples |
|---|---|---|
| Object and occurrence types | `snake_case` noun | `model_interaction`, `rag_retrieval` |
| Relationship and lineage types | `kebab-case` verb phrase read from source to target | `observed-in`, `evidence-for`, `derived-from` |
| Other enumerated values | `snake_case` | `completed`, `human_input` |
| Canonical event names | `aiops.<domain>.<past participle>` | `aiops.tool.completed` |
| Extension and extension event names | Reverse-domain, at least three segments, outside `aiops` | `org.example.support` |

Relationship types use hyphens so that a directional phrase such as
`delegated-to` cannot be mistaken for an object type. Values defined by an
external standard keep that standard's spelling: `currency` uses ISO 4217
upper-case codes (`USD`) and digest algorithms use their IANA names
(`sha-256`).

## Abbreviations

Names MUST spell words out. Only these abbreviations are permitted, because
each is more widely recognized than its expansion: `id`, `uri`, `rag`. Adding
one is a change to this document. Acronyms keep lower case inside names
(`rag_retrieval`, not `RAG_retrieval`).

## Catalog identifiers

Rule identifiers in machine-readable catalogs MUST match
`AIOS-<milestone>-<letter><two digits>`, for example `AIOS-0.4-P05` or
`AIOS-0.6-R03`. The letter names the rule family within that catalog. An
identifier is never reused for a different obligation, even after the rule it
named is withdrawn.

## Renaming

A rename of any published field, vocabulary member or event name is a
Breaking change under [v0.5 versioning](../v0.5/versioning.md). Before a
milestone freezes, a rename MAY still happen under the draft volatility rule,
but it MUST be recorded in [CHANGELOG.md](../../CHANGELOG.md).
