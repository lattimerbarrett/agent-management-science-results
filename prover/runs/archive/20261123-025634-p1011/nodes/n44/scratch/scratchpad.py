from pathlib import Path
p=Path('experiments/e3/agent3_local_pohozaev_bridge.md')
s=p.read_text()
print(s[14500:])
print('\n== Green/mass module ==\n')
print(Path('experiments/e3/agent4_green_mass_reduction.md').read_text())
print('\n== Files containing theorem references ==')
for p in Path('experiments/e3').glob('*.md'):
 s=p.read_text()
 lines=[x for x in s.splitlines() if any(w in x.lower() for w in ['marques','disconzi','khuri','almaraz','felli','ould','li–zhu','li-zhu'])]
 if lines: print(p.name, '\n'.join(lines)[:3000])
