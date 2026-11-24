from z3 import *
import itertools,time
open('workspace/agent4_rank33_obstruction.py','w').write(open(__file__).read())
# sixmaps coefficientlabels2..7, omitIlabel1
labs=[2,3,4,5,6,7]
lines=[frozenset([2+a,4+b,6+(a^b)]) for a,b in itertools.product(range(2),repeat=2)]
k=[Int('k%d'%x) for x in labs];ts=[Int('t%d'%i) for i in range(4)]
s=Solver();s.add(*[And(x>=0,x<=6) for x in k],*[And(x>=0,x<=7) for x in ts],Sum(ts)<=7)
def dim(S):
 if not S:return IntVal(7)
 if len(S)==1:return k[labs.index(next(iter(S)))]
 for i,line in enumerate(lines):
  if S<=line:return ts[i]
 return IntVal(0)
sets=[frozenset(labs[i] for i in range(6) if S>>i&1) for S in range(64)]
for A,B in itertools.product(sets,repeat=2):s.add(dim(A)+dim(B)<=dim(A&B)+dim(A|B))
# Ingleton forintersectionrankfunctions signflip inequality: dAB+dAC+dAD+dBC+dBD <=dA+dB+dCD+dABC+dABD
for a,b,c,d in itertools.permutations(range(6),4):
 A,B,C,D=[frozenset([labs[i]]) for i in [a,b,c,d]]
 s.add(dim(A|B)+dim(A|C)+dim(A|D)+dim(B|C)+dim(B|D)<=dim(A)+dim(B)+dim(C|D)+dim(A|B|C)+dim(A|B|D))
ps=[]
for i,x in enumerate(k+ts):
 y=Int('p%d'%i);s.add(Or(*[And(x==j,y==1<<j) for j in range(8)]));ps.append(y)
s.add(Sum(ps[:6])-2*Sum(ps[6:])==92)
t=time.time();r=s.check();print(r,time.time()-t)
if r==sat:print(s.model())
