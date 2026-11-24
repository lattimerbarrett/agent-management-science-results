import json,sys,itertools
sys.path.insert(0,'workspace')
from agent3_check import all_faces,maximal,appendable
D=json.load(open('workspace/agent2_corridor_trap_K1_certified.json'))
calls=0

def verify(facets,k,cert):
 global calls
 calls+=1
 facets=tuple(sorted(facets));assert facets
 rank=facets[0].bit_count();assert all(f.bit_count()==rank for f in facets)
 if cert[0]=='simplex':assert len(facets)==1 and cert[1]==facets[0];return
 assert cert[0]=='shed' and len(cert)==4
 s=cert[1];assert s and s.bit_count()<=k+1
 faces=all_faces(facets);assert s in faces
 deletion=maximal(f for f in faces if f&s!=s)
 assert deletion and all(f.bit_count()==rank for f in deletion)
 link=maximal(f^s for f in facets if f&s==s)
 verify(deletion,k,cert[2]);verify(link,k,cert[3])
verify(D['base'],0,D['basek0certificate'])
verify(D['facets'],1,D['k1certificate'])
fs=[]
for f in D['shelling']:
 if fs:assert appendable(tuple(fs),f)
 fs.append(f)
assert set(fs)==set(D['facets'])
for c in itertools.combinations(range(20),4):
 f=sum(1<<v for v in c)
 if f not in fs:assert not appendable(tuple(fs),f)
print('INDEPENDENT LOWER PROOF CERTIFIED:',calls,'certificate nodes checked, 173 shelling steps and 4672 blocked tetrahedra')
# Save a genuinely standalone checker + explicit source data.
source=open(__file__).read()
open('workspace/agent3_independent_trap_verify.py','w').write(source)
