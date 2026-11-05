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
        if not name or path.suffix not in {'.md', '.json'}:
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


if __name__ == '__main__':
    stage()
