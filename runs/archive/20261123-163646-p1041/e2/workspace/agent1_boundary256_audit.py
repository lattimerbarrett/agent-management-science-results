import json,sys,itertools,math, pathlib
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese

def rank(vs):
 B={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;break
 return len(B)

def audit():
 D=json.load(open('workspace/agent4_boundary256_orbits.json'));out=[]
 for a in D:
  if not a['solvable']:continue
  S=a['support'];T=sorted(set((p&63)|((p>>3)&64) for p in S)); assert len(T)==32
  dims=[len(T)-rank(veronese(7,e)[p] for p in T) for e in range(1,6)]
  assert dims==[24,8,1,0,0]
  K5=sum(math.comb(3,j)*dims[1+j] for j in range(4))
  assert K5==11
  arank=rank([1|(p<<1) for p in S]);assert arank==11
  out.append({'orbit':a['type'],'base_kernel_dims':dims,'tensor_K5':K5,'affine_dimension':arank})
  # Direct ten-dimensional rank, independent of tensor identity.
  direct=len(S)-rank(veronese(10,5)[p] for p in S);assert direct==11
 for n in range(1,101):
  for r in range(1,n+1):
   for j in range(1,n+2):
    assert j-1+n-min(n,r*j)>=math.ceil(n/r)-1
 for ell in range(1,20):
  for d in range(ell+1,25):
   target=2**d-2**ell
   assert 2**d-2**(ell-1)>=target
   assert 2*(2**(d-1)-2**(ell-1))==target
 assert math.comb(260,2)//18 < 2**11-1
 result={'boundary':out,'divisibility_valuations_checked':True,'general_radical_induction_checked':True,'w260_max_directions':math.comb(260,2)//18}
 json.dump(result,open('workspace/agent1_boundary256_audit.json','w'),indent=2);print(json.dumps(result,indent=2))

if __name__=='__main__':
 pathlib.Path('workspace/agent1_boundary256_audit.py').write_text(pathlib.Path(__file__).read_text())
 audit()
