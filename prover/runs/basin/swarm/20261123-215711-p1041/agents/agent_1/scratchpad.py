from pathlib import Path
import zipfile,hashlib
W=Path('workspace'); p=W/'RESULT.md';t=p.read_text();start=t.index('# Proof chapter 2: `agent4_proof_assembly.md`');end=t.index('\n\n---\n\n# Proof chapter 3:',start)
new='# Proof chapter 2: `agent4_proof_assembly.md`\n\n'+(W/'agent4_proof_assembly.md').read_text()
old=t[start:end]
print('Current chapter matches:',old==new)
if old!=new:
 t=t[:start]+new+t[end:];p.write_text(t)
 zpath=W/'reed_muller_codim7_complete.zip'
 with zipfile.ZipFile(zpath) as z:names=z.namelist()
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
  for name in names:z.write(Path(name),name)
 print('Updated proof article and bundle',len(p.read_bytes()),hashlib.sha256(p.read_bytes()).hexdigest())
