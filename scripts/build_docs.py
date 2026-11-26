"""Stage documentation from tracked sources; never publish a workspace walk."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys

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
    overview = STAGING / 'docs/index.md'
    if overview.is_file():
        # Like the product sites, the curated docs overview is the home page.
        # Rebase its docs/-relative links onto the site root it is served from.
        def rebase(match):
            target = match.group(1)
            if ':' in target or target.startswith('#'):
                return match.group(0)
            file_part, marker, anchor = target.partition('#')
            relative = os.path.relpath((overview.parent / file_part).resolve(), STAGING)
            return '](' + Path(relative).as_posix() + marker + anchor + ')'
        (STAGING / 'index.md').write_text(
            re.sub(r'\]\(([^)]+)\)', rebase, overview.read_text(encoding='utf-8')),
            encoding='utf-8',
        )
        overview.unlink()
        (STAGING / 'README.md').unlink()
    else:
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


def redirect(page: Path, target: str) -> None:
    """Write a static redirect that keeps the URL fragment (#anchor)."""
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0;url={target}">'
        f'<link rel="canonical" href="{target}"><title>AI Operations Specification</title>'
        f'<script>location.replace("{target}" + location.hash)</script>'
        f'</head><body><a href="{target}">Open AI Operations Specification documentation</a>'
        '</body></html>\n', encoding='utf-8',
    )


def page_url(relative: Path) -> str:
    """The directory URL MkDocs serves a staged Markdown page at."""
    parts = list(relative.with_suffix('').parts)
    if parts and parts[-1] in ('index', 'README'):
        parts.pop()
    return '/'.join(parts) + '/' if parts else ''


def publish_shared(site: Path, website: Path) -> None:
    """Publish the shared-theme site at docs/ and keep every earlier URL working.

    deepagentlabs.io/ai-operations-spec/ is this repository's Pages site, so
    it must publish the same shared-theme build the product sites use. The
    pages live under docs/ like every product. Schema $ids, catalogs and
    fixtures keep their root URLs, and earlier page URLs redirect to docs/.
    """
    builder = website / 'scripts/build_docs.py'
    if not builder.is_file():
        raise ValueError(f'Shared docs builder not found: {builder}')
    if site.exists():
        shutil.rmtree(site)
    subprocess.run(
        [sys.executable, str(builder), '--repo', str(ROOT),
         '--project', 'ai-operations-spec', '--output', str(site / 'docs')],
        check=True,
    )
    stage()
    for source in sorted(p for p in STAGING.rglob('*') if p.is_file()):
        relative = source.relative_to(STAGING)
        if source.suffix == '.md':
            url = page_url(relative)
            target = site / url / 'index.html'
            if not target.exists():
                depth = url.count('/')
                redirect(target, '../' * depth + 'docs/' + url)
        else:
            target = site / relative
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    # GitHub Pages serves the root 404 page for every missing URL; use the themed one.
    if (site / 'docs/404.html').is_file() and not (site / '404.html').exists():
        shutil.copyfile(site / 'docs/404.html', site / '404.html')
    # Earlier native sites served the raw AI reference at docs/llms-full.md;
    # the shared build publishes it at that same URL.
    if not (site / 'docs/llms-full.md').is_file():
        raise ValueError('Shared build did not publish docs/llms-full.md')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shared-site', type=Path, help='publish the shared-theme site here')
    parser.add_argument('--website', type=Path, help='deepagentlabs.github.io checkout')
    args = parser.parse_args()
    if args.shared_site is not None:
        if args.website is None:
            parser.error('--shared-site requires --website')
        publish_shared(args.shared_site.resolve(), args.website.resolve())
    else:
        stage()
