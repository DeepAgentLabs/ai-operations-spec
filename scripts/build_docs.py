"""Stage documentation from tracked sources; never publish a workspace walk."""
from pathlib import Path
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / '.docs-source'


def stage() -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir()
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=ROOT,
    ).decode().split('\0')
    for name in tracked:
        path = Path(name)
        if not name or (path.suffix not in {'.md', '.json'} and not (
            path.parts[:3] == ('docs', 'guide', 'examples') and path.suffix == '.py'
        )):
            continue
        if len(path.parts) > 1 and path.parts[0] not in {
            'specification', 'docs', 'reviews', 'drafts',
        }:
            continue
        source = ROOT / path
        if not source.is_file() or source.is_symlink():
            continue
        destination = STAGING / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    (STAGING / 'README.md').rename(STAGING / 'index.md')
    # MkDocs treats README and index as the same page. Normalize links to the
    # root overview; link code and directory references to the source browser.
    for markdown in STAGING.rglob('*.md'):
        if markdown.name == 'llms-full.md':
            continue  # Publish the generated reference verbatim; its checksum must match.
        def link(match):
            target = match.group(1)
            if ':' in target or target.startswith('#'):
                return match.group(0)
            file_part, marker, anchor = target.partition('#')
            resolved = (markdown.parent / file_part).resolve()
            if resolved == STAGING / 'README.md':
                replacement = os.path.relpath(STAGING / 'index.md', markdown.parent)
                return '](' + replacement + (marker + anchor if marker else '') + ')'
            if not resolved.is_file():
                try:
                    relative = resolved.relative_to(STAGING)
                except ValueError:
                    return match.group(0)
                source = ROOT / relative
                if source.exists():
                    kind = 'tree' if source.is_dir() else 'blob'
                    return f'](https://github.com/DeepAgentLabs/ai-operations-spec/{kind}/main/{relative}' + (marker + anchor if marker else '') + ')'
            return match.group(0)
        markdown.write_text(re.sub(r'\]\(([^)]+)\)', link, markdown.read_text()), encoding='utf-8')
    # Existing schema $ids predate the source-directory layout. Serve aliases
    # without changing their identity or rewriting $refs.
    for schemas in sorted((STAGING / 'specification').glob('v*/schemas')):
        shutil.copytree(schemas, STAGING / schemas.parent.name)


def publish_alias(site: Path) -> None:
    """Keep the shared /docs/ landing URL usable beside native document paths."""
    if not (site / 'index.html').is_file():
        raise ValueError('Build the documentation site before publishing aliases')
    target = site / 'docs/index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0;url=../">'
        '<link rel="canonical" href="../"><title>AI Operations Specification</title>'
        '</head><body><a href="../">Open AI Operations Specification documentation</a>'
        '</body></html>\n', encoding='utf-8',
    )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish-alias', type=Path)
    args = parser.parse_args()
    if args.publish_alias is not None:
        publish_alias(args.publish_alias)
    else:
        stage()
