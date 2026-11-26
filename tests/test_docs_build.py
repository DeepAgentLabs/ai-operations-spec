"""Guard the publication boundary and historical schema URLs."""
import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_staging_publishes_only_tracked_document_sources(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('build_docs', ROOT / 'scripts/build_docs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    tracked = {
        'README.md': '# Draft\n\n[Code](tests/check.py)\n',
        'docs/guide.md': '[Home](../README.md)\n',
        'docs/llms-full.md': '# Raw reference\n\n[Home](../README.md)\n',
        'docs/guide/examples/tutorial.py': 'print("tutorial")\n',
        'specification/v0.4/schemas/run.schema.json': '{"$id":"unchanged"}\n',
        'specification/v0.8/schemas/audit_event.schema.json': '{"$id":"operational"}\n',
        'tests/check.py': 'private implementation\n',
        'src/private.json': '{"not":"documentation"}',
    }
    for name, content in tracked.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    subprocess.run(['git', 'add', '.'], cwd=tmp_path, check=True)
    (tmp_path / 'docs/secret.md').write_text('untracked secret')
    (tmp_path / 'docs/link.md').symlink_to(tmp_path / 'tests/check.py')
    subprocess.run(['git', 'add', 'docs/link.md'], cwd=tmp_path, check=True)
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr(module, 'STAGING', tmp_path / '.docs-source')
    module.stage()
    staged = tmp_path / '.docs-source'
    assert not (staged / 'docs/secret.md').exists()
    assert not (staged / 'docs/link.md').exists()
    assert (staged / 'docs/llms-full.md').read_bytes() == (tmp_path / 'docs/llms-full.md').read_bytes()
    assert (staged / 'docs/guide/examples/tutorial.py').is_file()
    assert not (staged / 'tests').exists()
    assert not (staged / 'src').exists()
    assert '[Home](../index.md)' in (staged / 'docs/guide.md').read_text()
    assert '/blob/main/tests/check.py' in (staged / 'index.md').read_text()
    assert (staged / 'v0.4/run.schema.json').read_bytes() == (
        tmp_path / 'specification/v0.4/schemas/run.schema.json'
    ).read_bytes()
    assert (staged / 'v0.8/audit_event.schema.json').read_bytes() == (
        tmp_path / 'specification/v0.8/schemas/audit_event.schema.json'
    ).read_bytes()
    # Stale output cannot survive subsequent staging.
    (staged / 'stale.md').write_text('old')
    module.stage()
    assert not (staged / 'stale.md').exists()


def test_docs_overview_becomes_the_home_page_with_rebased_links(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('build_docs', ROOT / 'scripts/build_docs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    tracked = {
        'README.md': '# Repository readme\n',
        'docs/index.md': '# Overview\n\n[Guide](developer-guide.md#quickstart) · [Spec](../specification/v0.4/README.md) · [Web](https://example.com) · [Here](#start)\n',
        'docs/developer-guide.md': '# Guide\n\n[Home](../README.md)\n',
        'specification/v0.4/README.md': '# Schemas\n',
    }
    for name, content in tracked.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    subprocess.run(['git', 'add', '.'], cwd=tmp_path, check=True)
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr(module, 'STAGING', tmp_path / '.docs-source')
    module.stage()
    staged = tmp_path / '.docs-source'
    home = (staged / 'index.md').read_text()
    assert home.startswith('# Overview')
    assert '[Guide](docs/developer-guide.md#quickstart)' in home
    assert '[Spec](specification/v0.4/README.md)' in home
    assert '[Web](https://example.com)' in home and '[Here](#start)' in home
    assert not (staged / 'docs/index.md').exists()
    assert not (staged / 'README.md').exists()
    assert '[Home](../index.md)' in (staged / 'docs/developer-guide.md').read_text()


def test_public_landing_alias_preserves_native_guides_and_raw_reference(tmp_path):
    spec = importlib.util.spec_from_file_location('build_docs', ROOT / 'scripts/build_docs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / 'index.html').write_text('Native documentation home')
    (tmp_path / 'docs/developer-guide').mkdir(parents=True)
    guide = tmp_path / 'docs/developer-guide/index.html'
    guide.write_text('Native developer guide')
    reference = tmp_path / 'docs/llms-full.md'
    reference.write_bytes(b'# Exact reference snapshot\n')
    module.publish_alias(tmp_path)
    alias = (tmp_path / 'docs/index.html').read_text()
    assert 'content="0;url=../"' in alias
    assert '<a href="../">' in alias
    assert guide.read_text() == 'Native developer guide'
    assert reference.read_bytes() == b'# Exact reference snapshot\n'
