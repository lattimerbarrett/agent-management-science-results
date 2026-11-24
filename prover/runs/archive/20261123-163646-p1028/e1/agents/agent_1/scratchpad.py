from pathlib import Path
import hashlib,json,zipfile
base=Path('workspace/complete_certificate_agent1');p=base/'PROOF.md';s=p.read_text()
insert='''## Degree-four reduction at even orders
The four-regular analysis also bounds every pair, without assuming odd n, by R<=n/4-23/20 when a separating articulation exists, and by R<=max(n/8,3n/16-31/40) otherwise. These bounds are proved in Chapter3 before the odd-order residue optimization. Multiplying by4, each is strictly below 3n/2-33/4 for n>=10: the three comparisons reduce respectively to n/2>73/20, n>33/4, and3n/4>103/20. Thus degree4 cannot exceed either even-order cubic target. Together with Chapters4,5,6, this covers EVERY degree at even orders.

'''
s=s.replace('## Small editorial clarifications',insert+'## Small editorial clarifications');p.write_text(s)
manifest={str(f.relative_to(base)):hashlib.sha256(f.read_bytes()).hexdigest()for f in base.rglob('*')if f.is_file()and f.name!='SHA256.json'}
(base/'SHA256.json').write_text(json.dumps(manifest,indent=2))
for t in ['workspace/regular_graph_proof_certificate.zip','workspace/final_artifacts_agent1/regular_graph_proof_certificate.zip']:
 with zipfile.ZipFile(t,'w',zipfile.ZIP_DEFLATED)as z:
  for f in base.rglob('*'):
   if f.is_file():z.write(f,str(f.relative_to(base)))
print('Complete proof',len(s),'chars, all degree4-even comparisons integrated.')
