import sys,json,time,pickle
from collections import defaultdict
from fractions import Fraction
sys.path.insert(0,'workspace')
import agent1_hodge_mod as h
P=h.P
pd=json.load(open('workspace/agent2_P24.json'));ed=json.load(open('workspace/fz25_exceptional.json'))
pterms=[(tuple(a),h.Q(Fraction(c))) for a,c in pd['terms']]
evec=[int(v)%P for v in ed['vector']]
eterms=list(zip(map(tuple,ed['basis']),evec))
kp=defaultdict(int)
for a,c in pterms:
 for b,d in eterms:kp[tuple(sorted(a+b))]=(kp[tuple(sorted(a+b))]+c*d)%P
print('kappa support',len(kp),flush=True)
ps=defaultdict(int)
for a,c in kp.items():
 for b,d in h.kappa_expansion(a):ps[b]=(ps[b]+c*d)%P
ps={a:c for a,c in ps.items() if c}
print('psi support',len(ps),flush=True)
pickle.dump(ps,open('workspace/agent1_bulk_ps.pkl','wb'))
ls=h.lambda_expansion(23)
print('lambda support',len(ls),flush=True)
parts=[];ans=0;t0=time.time()
for j,(ms,c) in enumerate(ls):
 t=time.time();val=0
 for a,d in ps.items():val=(val+d*h.F(25,tuple(x+1 for x in a),ms))%P
 val=val*c%P;ans=(ans+val)%P
 parts.append([list(ms),val])
 print('DONE',j,ms,val,'SUM',ans,'time',round(time.time()-t,2),'total',round(time.time()-t0,2),h._F.cache_info(),flush=True)
 json.dump({'prime':P,'sum':ans,'parts':parts},open('workspace/agent1_bulk_partial.json','w'))
print('BULK',ans,'TOTAL', (ans+369940424)%P,flush=True)
