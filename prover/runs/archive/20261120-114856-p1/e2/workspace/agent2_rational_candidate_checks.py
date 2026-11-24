from sage.all import *
import json
from pathlib import Path
j=json.loads(Path('workspace/agent4_rationalized_mp.json').read_text())
from fractions import Fraction
def dec(s):
 ff=Fraction(s);return QQ(ff.numerator)/ff.denominator
def rnd(s,N=30):
 a=dec(s);den=ZZ(10)**N;return QQ(ZZ((a*den).round()))/den
P=PolynomialRing(QQ,'x');x=P.gen();pc=list(map(rnd,j['pc']));p=sum(pc[k]*x**(3-k)for k in range(4));c2=rnd(j['qc'][1]);eta=QQ(71)/100;xi=list(map(rnd,j['extra']));nodes=[eta]+xi
A=matrix(QQ,[[p(t)*t,p(t),-1 if k==0 else 1]for k,t in enumerate(nodes)]);B=vector(QQ,[-p(t)*(t**3+c2*t*t)for t in nodes]);c1,c0,h=A.solve_right(B);q=x**3+c2*x*x+c1*x+c0
assert p(eta)*q(eta)==h
for t in xi:assert p(t)*q(t)==-h
chi6=p*q-h;chi5,rem=chi6.quo_rem(x-eta);assert rem==0
R=RealIntervalField(200);roots=chi5.roots(AA);assert len(roots)==5 and all(m==1 for _,m in roots);core=[R(a)for a,m in roots];th=QQ(-82)/100
weights=[]
for k,t in enumerate(core):
 d=1/prod(t-core[l]for l in range(5)if l!=k);weights.append(d*q(t)*(t-th))
assert all(w.lower()>0 for w in weights)
assert (sum(weights)-1).contains_zero()
assert len(p.roots(AA))==3 and len(q.roots(AA))==3
full=chi5*prod(x-t for t in xi);assert len(full.roots(AA))==7
out={'p_ascending':[str(a)for a in p.list()],'q_ascending':[str(a)for a in q.list()],'h':str(h),'eta':str(eta),'extras':list(map(str,xi)),'chi5_ascending':[str(a)for a in chi5.list()],'theta':str(th),'word_left':[0,1],'word_right':[1]}
Path('workspace/agent2_fully_rational_candidate.json').write_text(json.dumps(out,indent=2))
print('h',R(h));print('core',core);print('extra',list(map(R,xi)));print('weightsatθ−.82',weights);print('p,q rationalized coeff differences',[(R(pc[k])-R(dec(j['pc'][k])))for k in range(4)],R(c1)-R(dec(j['qc'][2])),R(c0)-R(dec(j['qc'][3])));print('Exactall-rationalcandidatecertified,JSONsaved.')
