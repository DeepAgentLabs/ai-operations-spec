# Coordinated v1.0 engineering readiness

The repository's published schemas/catalogs remain unchanged at snapshot
v0.8.0. Lens 0.14.0 and MCP 0.8.0 implement all 66 portable outcome cases and
5 held-byte provenance-resolution cases using their own runtime code, without
importing repository test helpers. Both packages include pinned local schemas
and explicit marker routing. Sidecar 0.11.0/MCP 0.8.0 emit audit companions,
Lens 0.14.0 emits verification signals, and Tower 0.11.0 emits investigation
reports from native objects. These are implementation releases, not new AIOS
schema markers or stable conformance claims.

The source-built wheel matrix runs with Python -I from empty workspaces, checks
installed import origins and tests unavailable-as-pass, unsupported markers,
missing citations and native outcome boundaries. It supplies internal engineering
evidence. The decision D-001 independence requirement, independent producer/
validator evidence and maintainer confirmation remain open. Neither shared
code authorship nor Copilot review establishes independence.

Operational adoption is optional and existing artifacts remain valid. Consumers
that do not implement these schemas continue rejecting unsupported markers.
This documentation/evidence alignment requires no new specification release.

Independent acceptance, live/deployment evidence and the stable freeze remain
separate gates. See the [shared release policy](https://github.com/DeepAgentLabs/.github/blob/main/profile/RELEASE_POLICY.md).

Repository v0.8.1 adds the MIT license and this evidence/adoption guidance. Schema bytes, markers, rule catalogs and portable outcomes are unchanged from v0.8.0.
