from pathlib import Path
p=Path('experiments/e1')
for name in ['agent4_H4_torsion_centrality.json','agent2_cover_class3_invariants.json','agent3_mod9_gamma5_invariants.json','agent3_mod27_gamma5_invariants.json']:
 f=p/name
 if f.exists(): print(name,f.read_text()[:5000])
for f in p.glob('*.py'):
 s=f.read_text()
 if any(x in s.lower() for x in ['propagat','barthol','andreadakis conjecture holds','satoh','pettet']): print(f.name,[(s[max(0,i-100):i+200]) for i in [s.lower().find('propagat'),s.lower().find('barthol'),s.lower().find('satoh')] if i>=0])