from pathlib import Path
for name in ['experiments/e5/agent1_verified_partial.txt','experiments/e5/agent3_worm_proof.md','experiments/e2/agent2_shifted_pole_lemma.txt']:
 p=Path(name)
 print('\n===== '+name+' =====\n'+p.read_text()[:22000])
print('\n===== STEIN-BASIS DISCUSSIONS =====')
for d in ['e2','e5','e6']:
 for p in Path('experiments',d).rglob('*'):
  if p.is_file() and p.suffix in ['.txt','.md']:
   text=p.read_text(errors='replace')
   lines=text.splitlines()
   inds=[i for i,l in enumerate(lines) if ('stein' in l.lower() and any(k in l.lower() for k in ['basis','neighborhood','neighbourhood']))]
   for i in inds[:4]:
    print(str(p)+': '+ '\n'.join(lines[max(0,i-1):min(len(lines),i+3)]))
