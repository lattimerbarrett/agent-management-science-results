from sage.all import *
import json
out=[]
x=polygen(QQ)
for c in [4,8,12,16,20,24,28,32]:
 d=c//4
 K=NumberField(x**(2*d)-2*x**d+2,'pi'); pi=K.gen(); P=K.ideal(pi)
 assert P.is_prime() and P.norm()==2
 i=1-pi**d
 assert i*i==-1
 vals=[int(K.hilbert_symbol(1+pi,1+sg*pi**(c-1),P)) for sg in [1,-1]]
 assert vals==[-1,-1]
 out.append(dict(c=c,degree=int(K.degree()),symbols=vals));print(out[-1],flush=True)
json.dump(out,open('workspace/agent2_hilbert_checks.json','w'))
