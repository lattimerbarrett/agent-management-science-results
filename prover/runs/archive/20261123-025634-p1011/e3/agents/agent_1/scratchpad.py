from pathlib import Path
import zipfile, hashlib
root=Path('workspace/boundary_yamabe_verified')
manifest=[]
for p in sorted(root.rglob('*')):
 if p.is_file() and '__pycache__' not in str(p):
  manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(root)))
(root/'SHA256SUMS').write_text('\n'.join(manifest)+'\n')
out=Path('workspace/boundary_yamabe_verified.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if p.is_file() and '__pycache__' not in str(p):z.write(p,p.relative_to(root))
print('Bundle:',out,'bytes',out.stat().st_size)
print('SHA256:',hashlib.sha256(out.read_bytes()).hexdigest())
