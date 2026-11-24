import itertools,json
from pathlib import Path

def red(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inv(w):return tuple(-x for x in w[::-1])
def sub(w,A):
 s=()
 for x in w:s=red(s+(A[x-1] if x>0 else inv(A[-x-1])))
 return s
def comp(A,B):return tuple(sub(w,A) for w in B)
def gens(n):
 I=tuple((i,) for i in range(1,n+1));G=[];Gi=[];names=[]
 for i in range(1,n+1):
  for j in range(1,n+1):
   if i==j:continue
   A=list(I);B=list(I);A[i-1]=(j,i,-j);B[i-1]=(-j,i,j);G.append(tuple(A));Gi.append(tuple(B));names.append(('K',i,j))
  for j,k in itertools.combinations([x for x in range(1,n+1) if x!=i],2):
   A=list(I);B=list(I);A[i-1]=(j,k,-j,-k,i);B[i-1]=(k,j,-k,-j,i);G.append(tuple(A));Gi.append(tuple(B));names.append(('M',i,j,k))
 return G,Gi,names
res=json.load(open('workspace/agent2_true_relations.json'))
for data in res:
 G,Gi,names=gens(data['n']);assert [list(x) for x in names]==data['names']
 for i,j,k,sgn in data['relations']:
  A=G[i];B=comp(G[j],G[k] if sgn==1 else Gi[k]);assert comp(A,B)==comp(B,A)
 print('exact relators verified n',data['n'])
n=6;G,Gi,names=gens(n);m=len(G);rels=[]
for j in range(m):
 for k in range(j,m):
  for sgn in [1,-1]:
   B=comp(G[j],G[k] if sgn==1 else Gi[k])
   for i in range(m):
    if (i==j and i==k):continue
    if comp(G[i],B)==comp(B,G[i]):rels.append((i,j,k,sgn))
r2=n*n*(n*n-1)//3-n*(n+1)//2
print('n6 relations',len(rels))
res.append({'n':n,'names':names,'relations':rels,'needed':m*(m-1)//2-r2})
Path('workspace/agent2_true_relations6.json').write_text(json.dumps(res))
