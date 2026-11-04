#!/usr/bin/env python3
"""Validate the public skill index and marketplace paths. Standard library only."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
catalog=json.loads((ROOT/'catalog.json').read_text())
roles={r['slug'] for r in catalog['roles']}
seen=set()
for skill in catalog['skills']:
    name=skill['name']
    assert name not in seen and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name),name
    seen.add(name)
    path=(ROOT/skill['path']).resolve()
    assert ROOT in path.parents and path.is_file(),skill['path']
    text=path.read_text()
    assert re.search(r'^name: '+re.escape(name)+r'$',text,re.M),name
    assert skill['role'] in roles,name
    assert name in next(r for r in catalog['roles'] if r['slug']==skill['role'])['skills'],name
    assert (path.parent/'agents/openai.yaml').is_file(),name
files={str(p.relative_to(ROOT)) for p in (ROOT/'plugins').rglob('SKILL.md')}
assert files=={s['path'] for s in catalog['skills']},'Unindexed or missing skills'
manifest=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
for plugin in manifest['plugins']:
    source=(ROOT/plugin['source']).resolve()
    assert ROOT in source.parents and source.is_dir(),plugin
    assert (source/'.claude-plugin/plugin.json').is_file(),plugin
print(f"Validated {len(seen)} skills, {len(roles)} roles and marketplace source paths")
