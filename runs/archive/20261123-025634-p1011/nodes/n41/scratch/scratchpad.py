from pathlib import Path
p=Path('experiments/e3')
for f in p.iterdir():
 if any(s in f.name for s in ['certificate','verify','positiv','uniform','profile','minor','bundle']): print(f.name,f.stat().st_size)
print('\nLOCAL PROOF BEGIN\n')
t=p.joinpath('agent3_local_pohozaev_bridge.md').read_text()
print(t[:16000])
