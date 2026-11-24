import json,time

def inv(w):return tuple(-i for i in w[::-1])
def cat(*ws):
 z=[]
 for w in ws:
  for x in w:
   if z and z[-1]==-x:z.pop()
   else:z.append(x)
 return tuple(z)
def subst(w,A):return cat(*(A[x-1] if x>0 else inv(A[-x-1]) for x in w))
def compose(A,B):return tuple(subst(w,A) for w in B)
def inverse_aut(A):
 n=len(A);I=tuple((i+1,) for i in range(n))
 if all(len(w)==1 for w in A):
  B=[None]*n
  for i,(x,) in enumerate(A):B[abs(x)-1]=((i+1)*(1 if x>0 else -1),)
 else:
  changed=[i for i in range(n) if A[i]!=I[i]];assert len(changed)==1
  i=changed[0];w=A[i];j=w.index(i+1);assert sum(abs(x)==i+1 for x in w)==1
  B=list(I);B[i]=cat(inv(w[:j]),(i+1,),inv(w[j+1:]))
 B=tuple(B);assert compose(A,B)==compose(B,A)==I
 return B
def run(path='workspace/agent1_gap_ia4_data.json'):
 data=json.load(open(path));n=data['n'];I=tuple((i+1,) for i in range(n));gs=[tuple(map(tuple,a)) for a in data['generator_images']];gis=[inverse_aut(a) for a in gs]
 def evaluate(w):
  A=I
  for x in w:A=compose((gs if x>0 else gis)[abs(x)-1],A)
  return A
 start=time.time()
 for k,r in enumerate(data['rels']):
  assert evaluate(r)==I,('badseed',k)
  if k%100==0:print('verifiedseed',k,flush=True)
 for e,(phi,sim) in enumerate(zip(data['endomorphisms'],data['Gendos'])):
  S=tuple(map(tuple,sim));Si=inverse_aut(S)
  for i,w in enumerate(phi):assert evaluate(w)==compose(compose(S,gs[i]),Si),('badendo',e,i)
 print('ALL actualIA4identitiesverified',len(data['rels']),'seeds',len(data['endomorphisms'])*len(gs),'endoimages',time.time()-start,flush=True)
if __name__=='__main__':run()
