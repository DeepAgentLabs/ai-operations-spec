"""Generate docs/api-reference.md from the published schemas and rule catalogs.

AIOS has no runtime API; its public surface is the artifact contract. Rendering
the reference from the schemas keeps field tables from drifting. Any schema
keyword the renderer does not understand is an error rather than silently
omitted, so a schema change cannot quietly drop a constraint from the page.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/api-reference.md"

# (title, schema, example, prose, catalog) in reading order.
FAMILIES = [
    ("Run", "specification/v0.4/schemas/run.schema.json",
     "specification/v0.4/examples/valid/run.json", "specification/v0.4/README.md",
     "specification/v0.4/conformance-rules.json"),
    ("Workflow", "specification/v0.4/schemas/workflow.schema.json",
     "specification/v0.4/examples/valid/workflow.json", "specification/v0.4/README.md",
     "specification/v0.4/conformance-rules.json"),
    ("Provenance record", "specification/v0.6/schemas/provenance.schema.json",
     "specification/v0.6/examples/provenance/support-finding.provenance.json",
     "specification/v0.6/provenance.md", "specification/v0.6/provenance-rules.json"),
    ("Verification signal", "specification/v0.8/schemas/verification_signal.schema.json",
     "specification/v0.8/examples/verification_signal.json",
     "specification/v0.8/verification-signals.md", "specification/v0.8/operational-rules.json"),
    ("Audit event", "specification/v0.8/schemas/audit_event.schema.json",
     "specification/v0.8/examples/audit_event.json",
     "specification/v0.8/audit-events.md", "specification/v0.8/operational-rules.json"),
    ("Investigation report", "specification/v0.8/schemas/investigation_report.schema.json",
     "specification/v0.8/examples/investigation_report.json",
     "specification/v0.8/investigation-reports.md", "specification/v0.8/operational-rules.json"),
]
SHARED = [
    ("Shared definitions: 0.4-draft", "specification/v0.4/schemas/common.schema.json"),
    ("Shared definitions: 0.8-draft", "specification/v0.8/schemas/common.schema.json"),
]
CATALOGS = [
    ("Run and Workflow", "specification/v0.4/conformance-rules.json"),
    ("Provenance", "specification/v0.6/provenance-rules.json"),
    ("Operational artifacts", "specification/v0.8/operational-rules.json"),
]
PROFILES = [
    ("Access evidence", "drafts/access-evidence-v1/access.schema.json", "drafts/access-evidence-v1/README.md"),
    ("Sidecar correlation", "drafts/sidecar-correlation-v1/schema.json", "drafts/sidecar-correlation-v1/README.md"),
    ("Sidecar intent", "drafts/sidecar-contracts-v1/intent.schema.json", "drafts/sidecar-contracts-v1/README.md"),
    ("Sidecar decision", "drafts/sidecar-contracts-v1/decision.schema.json", "drafts/sidecar-contracts-v1/README.md"),
    ("Sidecar audit", "drafts/sidecar-contracts-v1/audit.schema.json", "drafts/sidecar-contracts-v1/README.md"),
    ("Sidecar scope", "drafts/sidecar-contracts-v1/scope.schema.json", "drafts/sidecar-contracts-v1/README.md"),
    ("Sidecar transfer", "drafts/sidecar-contracts-v1/transfer.schema.json", "drafts/sidecar-contracts-v1/README.md"),
]

ANNOTATIONS = {"$schema", "$id", "$comment", "title", "description", "default", "$defs"}
VALUE = {"$ref", "const", "enum", "type", "items", "properties", "required", "additionalProperties",
         "format", "pattern", "minLength", "maxLength", "minimum", "maximum", "minItems",
         "maxItems", "uniqueItems", "propertyNames", "anyOf", "oneOf", "allOf", "not",
         "if", "then", "else"}


def code(value) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return "`" + text.replace("|", "\\|") + "`"


def link(relative: str) -> str:
    return "../" + relative


def anchor(path: str, name: str | None = None) -> str:
    version = next(part for part in Path(path).parts if part.startswith("v0."))
    stem = Path(path).name.split(".")[0]
    base = f"{version.replace('.', '')}-{stem}".replace("_", "-")
    return base + ("-" + name.replace("_", "-") if name else "")


class Renderer:
    def __init__(self):
        self.files = {}
        for relative in [f[1] for f in FAMILIES] + [s[1] for s in SHARED]:
            schema = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.files[schema["$id"]] = (relative, schema)

    def check(self, node, where):
        unknown = set(node) - ANNOTATIONS - VALUE
        if unknown:
            raise ValueError(f"Unrendered schema keywords at {where}: {sorted(unknown)}")

    def resolve(self, ref, base):
        target, _, pointer = urljoin(base, ref).partition("#")
        relative, schema = self.files[target]
        if not pointer:
            return relative, None, schema
        parts = pointer.strip("/").split("/")
        if parts[0] != "$defs" or len(parts) != 2:
            raise ValueError(f"Unsupported reference: {ref}")
        return relative, parts[1], schema["$defs"][parts[1]]

    def type_of(self, node, base) -> str:
        if "$ref" in node:
            relative, name, _ = self.resolve(node["$ref"], base)
            return f"[`{name}`](#{anchor(relative, name)})"
        if "const" in node:
            return "const"
        if "enum" in node:
            return "enum"
        for key in ("anyOf", "oneOf"):
            if key in node and not any("required" in branch for branch in node[key]):
                return " or ".join(self.type_of(branch, base) for branch in node[key])
        kind = node.get("type")
        if kind == "array" or (kind is None and "items" in node):
            return "array of " + (self.type_of(node["items"], base) if "items" in node else "any")
        if isinstance(kind, list):
            return " or ".join(kind)
        return kind or ("object" if "properties" in node else "any")

    def limits(self, node, base) -> list[str]:
        out = []
        if "const" in node:
            out.append("always " + code(node["const"]))
        if "enum" in node:
            out.append("one of " + ", ".join(code(v) for v in node["enum"]))
        if "format" in node:
            out.append("format " + code(node["format"]))
        if "pattern" in node:
            out.append("pattern " + code(node["pattern"]))
        for key, label in (("minLength", "min length"), ("maxLength", "max length"),
                           ("minimum", "≥"), ("maximum", "≤"),
                           ("minItems", "min items"), ("maxItems", "max items")):
            if key in node:
                out.append(f"{label} {node[key]}")
        if node.get("uniqueItems"):
            out.append("unique items")
        if "default" in node:
            out.append("default " + code(node["default"]))
        if "propertyNames" in node:
            out.append("keys: " + self.type_of(node["propertyNames"], base))
        items = node.get("items")
        if isinstance(items, dict) and "$ref" not in items and "properties" not in items:
            inner = self.limits(items, base)
            if inner:
                out.append("each item: " + "; ".join(inner))
        return out

    def rows(self, node, base, prefix=""):
        """Yield table rows; inline objects flatten into dotted field names."""
        self.check(node, prefix or "root")
        required = set(node.get("required", []))
        for name, child in node.get("properties", {}).items():
            self.check(child, prefix + name)
            field = prefix + name
            yield field, self.type_of(child, base), name in required, self.limits(child, base)
            target = child.get("items", child) if child.get("type") == "array" else child
            if "properties" in target and "$ref" not in target:
                suffix = "[]." if target is not child else "."
                yield from self.rows(target, base, field + suffix)

    def conditions(self, node, base, prefix=""):
        out = []
        for branch in node.get("allOf", []):
            if "if" in branch:
                out.append(self.conditional(branch, prefix))
            else:
                out.extend(self.facts(branch, prefix))
        if "if" in node:
            out.append(self.conditional(node, prefix))
        for key in ("anyOf", "oneOf"):
            if key in node and all("required" in branch for branch in node[key]):
                out.extend(self.facts({key: node[key]}, prefix))
        if "not" in node:
            out.extend(self.facts({"not": node["not"]}, prefix))
        for name, child in node.get("properties", {}).items():
            target = child.get("items", child) if child.get("type") == "array" else child
            if "$ref" not in target and ("allOf" in target or "if" in target):
                out.extend(self.conditions(target, base, prefix + name + ("[]." if target is not child else ".")))
        return out

    def conditional(self, branch, prefix):
        text = "If " + " and ".join(self.facts(branch["if"], prefix) or ["always"])
        text += ": " + "; ".join(self.facts(branch.get("then", {}), prefix) or ["no further constraint"])
        if "else" in branch:
            text += ". Otherwise: " + "; ".join(self.facts(branch["else"], prefix))
        return text + "."

    def facts(self, node, prefix):
        out = [f"{code(prefix + name)} is present" for name in node.get("required", [])]
        for name, child in node.get("properties", {}).items():
            field = prefix + name
            if "const" in child:
                out.append(f"{code(field)} is {code(child['const'])}")
            elif "enum" in child:
                out.append(f"{code(field)} is one of " + ", ".join(code(v) for v in child["enum"]))
            elif "type" in child and child["type"] != "array":
                out.append(f"{code(field)} is {child['type'] if isinstance(child['type'], str) else ' or '.join(child['type'])}")
            if "minLength" in child and child.get("minLength") == child.get("maxLength"):
                out.append(f"{code(field)} is exactly {child['minLength']} characters")
            else:
                if "minLength" in child:
                    out.append(f"{code(field)} has at least {child['minLength']} characters")
                if "maxLength" in child:
                    out.append(f"{code(field)} has at most {child['maxLength']} characters")
            if "pattern" in child:
                out.append(f"{code(field)} matches {code(child['pattern'])}")
            if child.get("maxItems") == 0:
                out.append(f"{code(field)} is empty")
            elif "maxItems" in child:
                out.append(f"{code(field)} has at most {child['maxItems']} items")
            if "minItems" in child:
                out.append(f"{code(field)} has at least {child['minItems']} item" + ("s" if child["minItems"] != 1 else ""))
            if "properties" in child or "required" in child:
                out.extend(self.facts(child, field + "."))
        for key, joiner in (("anyOf", "at least one of"), ("oneOf", "exactly one of")):
            if key in node:
                groups = [" and ".join(code(prefix + n) for n in b.get("required", [])) for b in node[key]]
                out.append(f"{joiner} " + ", ".join(groups) + " is present")
        if "not" in node:
            out.extend(f"{code(prefix + name)} is absent" for name in node["not"].get("required", []))
        if "allOf" in node:
            for branch in node["allOf"]:
                out.extend(self.facts(branch, prefix))
        return out

    def object_block(self, node, base) -> list[str]:
        lines = []
        if "properties" in node:
            lines += ["| Field | Type | Required | Constraints |", "| --- | --- | --- | --- |"]
            for field, kind, required, limits in self.rows(node, base):
                lines.append(f"| {code(field)} | {kind} | {'yes' if required else ''} | {'; '.join(limits)} |")
            lines.append("")
            if node.get("additionalProperties") is False:
                lines += ["Other fields: not allowed (`additionalProperties: false`).", ""]
        else:
            self.check(node, base)
            summary = "; ".join(self.limits(node, base))
            lines += [f"Type: {self.type_of(node, base)}" + (f". Constraints: {summary}." if summary else "."), ""]
        conditions = self.conditions(node, base)
        if conditions:
            lines += ["Conditional requirements:", ""] + [f"- {c}" for c in conditions] + [""]
        return lines

    def definitions(self, relative, schema, level="###") -> list[str]:
        lines = []
        for name, node in schema.get("$defs", {}).items():
            lines += [f'<a id="{anchor(relative, name)}"></a>', "", f"{level} `{name}`", ""]
            if "description" in node:
                lines += [node["description"], ""]
            lines += self.object_block(node, schema["$id"])
        return lines


def rules_by_family():
    found = {}
    for _, relative in CATALOGS:
        for rule in json.loads((ROOT / relative).read_text(encoding="utf-8"))["rules"]:
            for family in rule["applies_to"]:
                found.setdefault(family, []).append(rule["id"])
    return found


def render() -> str:
    renderer = Renderer()
    # tomllib is 3.11+; the repository supports 3.10.
    version = re.search(r'^version\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.M).group(1)
    applies = rules_by_family()
    out = [
        "# API Reference (detailed)",
        "",
        f"**Repository version:** {version}",
        "",
        "AIOS is a contract: its public interface is the set of JSON artifacts that producers emit and",
        "consumers accept. This page lists every field, type, constraint and conformance rule of each",
        "artifact family.",
        "",
        "All six artifact families ship with JSON Schemas, rule catalogs, canonical examples and the",
        "portable conformance suite. Each artifact declares its family's version marker exactly as shown",
        "(`0.4-draft`, `0.6-draft` or `0.8-draft`). The specification prose and rule catalogs define the",
        "full requirements: schemas check structure, and the conformance suite checks the semantic rules.",
        "",
        "This page is generated from the schemas and rule catalogs by `scripts/build_api_reference.py`.",
        "Edit those sources, then run `make api-reference`; a test fails if this page is stale.",
        "For a guided path, start with the [Developer Guide](developer-guide.md).",
        "",
        "## Artifact families",
        "",
        "| Family | Artifact type | Version marker | Schema | Example | Rules |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for title, schema_path, example, _, catalog in FAMILIES:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        props = schema["properties"]
        kind = props["artifact_type"].get("const") or "/".join(props["artifact_type"]["enum"])
        rules = applies.get(kind, [])
        out.append(
            f"| [{title}](#{anchor(schema_path)}) | {code(kind)} | {code(props['spec_version']['const'])} "
            f"| [{Path(schema_path).name}]({link(schema_path)}) | [{Path(example).name}]({link(example)}) "
            f"| {len(rules)} ([catalog](#{anchor(catalog)})) |"
        )
    out += [
        "",
        "How to read the field tables: a dotted name (`grounding.status`) is a field of an inline object,",
        "and `[]` marks the items of an array. Linked types are definitions listed under the family or",
        "under the shared definitions. To validate offline, register both shared schemas by `$id`; see",
        "[Offline structural validation](developer-guide.md#structural-validation).",
        "",
    ]
    for title, schema_path, example, prose, catalog in FAMILIES:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        kind = schema["properties"]["artifact_type"].get("const")
        rules = applies.get(kind, [])
        out += [
            f'<a id="{anchor(schema_path)}"></a>', "",
            f"## Artifact: {title}", "",
            f"`artifact_type: {kind}` · `spec_version: {schema['properties']['spec_version']['const']}` · "
            f"schema `{schema['$id']}`", "",
            f"Normative text: [{Path(prose).name}]({link(prose)}). "
            f"Example: [{Path(example).name}]({link(example)}).", "",
        ]
        if schema.get("description"):
            out += [schema["description"], ""]
        if rules:
            out += [f"Rules that apply ({len(rules)}): " + ", ".join(f"[{r}](#{r.lower()})" for r in rules) + ".", ""]
        out += [f"### {title} fields", ""] + renderer.object_block(schema, schema["$id"])
        out += renderer.definitions(schema_path, schema, "####") if schema.get("$defs") else []
    for title, schema_path in SHARED:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        out += [
            f"## {title}", "",
            f"Schema `{schema['$id']}` ([{Path(schema_path).name}]({link(schema_path)})).", "",
        ] + renderer.definitions(schema_path, schema)
    out += [
        "## Conformance rules", "",
        "Each rule has a stable ID that validators report. **Check** says how a rule is decided:",
        "`schema` and `semantic` from one artifact, `cross_artifact` across held artifacts, `process`",
        "from implementation behavior that no single artifact can show.", "",
    ]
    for title, catalog in CATALOGS:
        data = json.loads((ROOT / catalog).read_text(encoding="utf-8"))
        out += [
            f'<a id="{anchor(catalog)}"></a>', "",
            f"### Rules: {title} ({data['spec_version']})", "",
            f"Source: [{Path(data['source']).name}]({link(data['source'])}) · catalog "
            f"[{Path(catalog).name}]({link(catalog)})", "",
            "| ID | Role | Level | Check | Applies to | Requirement |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for rule in data["rules"]:
            requirement = rule["requirement"].replace("|", "\\|")
            out.append(
                f'| <a id="{rule["id"].lower()}"></a>`{rule["id"]}` | {rule["role"]} | {rule["level"]} '
                f'| {rule["check"]} | {", ".join(rule["applies_to"])} | {requirement} |'
            )
        out.append("")
    out += [
        "## Companion profiles (non-normative)", "",
        "These profiles extend the families above for access evidence and Sidecar integration. Each has",
        "its own schema and guide; they add no conformance rules and do not change the core families.", "",
        "| Profile | Schema | Guide |", "| --- | --- | --- |",
    ]
    for title, schema_path, guide in PROFILES:
        if not (ROOT / schema_path).is_file():
            raise ValueError(f"Missing profile schema: {schema_path}")
        out.append(f"| {title} | [{Path(schema_path).name}]({link(schema_path)}) | [README]({link(guide)}) |")
    return "\n".join(out).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if docs/api-reference.md is stale")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("docs/api-reference.md is stale; run: make api-reference")
    else:
        OUTPUT.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
