from pathlib import Path
import zipfile,hashlib,json
zpath=Path('workspace/agent1_complete_certificate_bundle.zip')
with zipfile.ZipFile(zpath) as z:
 data={f:z.read(f) for f in z.namelist()}
for f in data:
 if f!='README.txt' and Path('workspace',f).exists():data[f]=Path('workspace',f).read_bytes()
M=json.loads(data['agent1_complete_manifest.json'])
M['sha256']={f:hashlib.sha256(b).hexdigest() for f,b in data.items() if f not in ['README.txt','agent1_complete_manifest.json']}
data['agent1_complete_manifest.json']=json.dumps(M,indent=2).encode();Path('workspace/agent1_complete_manifest.json').write_bytes(data['agent1_complete_manifest.json'])
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for f,b in data.items():z.writestr(f,b)
print(zpath.stat().st_size,hashlib.sha256(zpath.read_bytes()).hexdigest())
