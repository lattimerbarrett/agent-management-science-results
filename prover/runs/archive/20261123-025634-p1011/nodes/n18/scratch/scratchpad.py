from pathlib import Path
for name in ['experiments/e3/agent3_local_pohozaev_bridge.md','experiments/e3/agent4_green_mass_reduction.md','experiments/e3/boundary_yamabe_verified/README.txt']:
    p=Path(name)
    print('\n###',name)
    text=p.read_text()
    print(text[:17000])
print('\n### Citation-like lines in experiment notes')
seen=set()
for p in Path('experiments').rglob('*'):
    if not p.is_file() or p.suffix not in ('.md','.txt'):continue
    if 'boundary_yamabe_verified/workspace' in str(p):continue
    for line in p.read_text(errors='ignore').splitlines():
        if any(w in line.lower() for w in ['li–zhu','li-zhu','han–li','han-li','felli','disconzi','marques','citation','scalar-flat']):
            line=line[:600]
            if line not in seen:
                seen.add(line)
                print(str(p)+': '+line)
                if len(seen)>100:break
    if len(seen)>100:break
