import pathlib,json,sys,itertools,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure
s=pathlib.Path('workspace/agent1_E256_P32_new320.py').read_text();exec(s[:s.index('obj=next')])
raw=json.load(open('workspace/agent4_boundary256_orbits.json'));out=[]
for obj in raw:
 if not obj['solvable']:continue
 S=sorted({(p&63)|((p>>3)&64) for p in obj['support']});X,r=closure(set(S),veronese(7,2));E0=sorted(p for p,c in X);B,K=basis(veronese(7,3)[p] for p in S);RR=[red(veronese(7,3)[p],B)[0] for p in E0];B,KB=basis(RR);assert len(KB)==7;C=[0]
 for u in KB:C +=[z^u for z in C]
 W=collections.Counter(x.bit_count() for x in C);assert W=={0:1,4:8,6:16,8:78,10:16,12:8,16:1}
 n=0;mins=17
 for a,b,c in itertools.combinations(C[1:],3):
  if a^b==c:continue
  k=(a|b|c).bit_count();mins=min(mins,k)
  if k==8:n+=1
 assert n==0
 out.append({'type':obj['type'],'three_indep_triples_union8':n,'minimum_union_of_3D_subcode':mins,'weight_enum':dict(W)});print(out[-1])
json.dump(out,open('workspace/agent1_E256_P32_period_audit.json','w'));pathlib.Path('workspace/agent1_E256_P32_period_audit.py').write_text(pathlib.Path(__file__).read_text())
