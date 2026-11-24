from pathlib import Path
# Exact target-word verification, independent of derivation calculations.
def red(w):
 z=[]
 for a in w:
  if z and z[-1]==a:z.pop()
  else:z.append(a)
 return tuple(z)
def inv(w):return w[::-1]
def prod(a,b):return red(a+b)
def comm(a,b):return red(a+b+inv(a)+inv(b))
def power(a,k):
 if k<0:a=inv(a);k=-k
 z=()
 for _ in range(k):z=prod(z,a)
 return z
A=(0,);B=(1,);C=(2,)
g=[B,A,A+B,C,A,A+C,C,B,B+C]
def V(i,j,k):return comm(comm(g[i],g[j]),g[k])
terms=[(3,(0,5,2)),(-1,(0,2,5)),(-4,(0,1,1)),(-2,(1,2,3))]
w=()
for c,t in terms:w=prod(w,power(V(*t),c))
print('reduced target wordlength',len(w))
P={()}
for a in w:
 Q=set(P)
 for v in P:
  if len(v)<3 and (not v or v[-1]!=a):Q.symmetric_difference_update([v+(a,)])
 P=Q
print('target Magnus terms',[''.join('ABC'[i] for i in v) for v in sorted(P,key=lambda w:(len(w),w))]);assert {v for v in P if len(v)==3}=={(0,2,1),(1,0,2),(1,2,0),(2,0,1)}
