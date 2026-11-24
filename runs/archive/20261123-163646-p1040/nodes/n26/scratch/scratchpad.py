from pathlib import Path
# Explicit obstruction to the proposed compression retraction, x=1,y=2,z=3.
def red(w):
 s=[]
 for a in w:
  if s and s[-1]==-a:s.pop()
  else:s.append(a)
 return s
def inv(w):return [-a for a in w[::-1]]
def apply(f,w):
 out=[]
 for a in w:out+=f[a] if a>0 else inv(f[-a])
 return red(out)
p=lambda w:red([a for a in w if abs(a)!=3])
alpha={1:[3,1,-3],2:[2],3:[3]}
beta={1:[1],2:[2],3:[1,2,-1,-2,3]}
print('compressed alpha:',[p(alpha[i]) for i in (1,2)])
print('compressed beta:',[p(beta[i]) for i in (1,2)])
print('compressed beta o alpha:',[p(apply(beta,alpha[i])) for i in (1,2)])
print('\nE2 companion filtration proof:\n')
print(Path('experiments/e2/agent4_metaplectic_filtration.txt').read_text())