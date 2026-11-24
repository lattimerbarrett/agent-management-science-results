import pickle,itertools,numpy as np,collections,math
# Independently reconstruct and verify every central-interval seed.
def pts(bs):
 s={0}
 for b in bs:s|={x^b for x in s}
 return s
def make(p):
 a,b,c,t,d,aff=p;bs=[[],[],[]];pos=0
 def block(k,ids):
  nonlocal pos
  z=[1<<(pos+i) for i in range(k)];pos+=k
  for j in ids:bs[j]+=z
  return z
 block(t,[0,1,2]);block(a-t,[0,1]);block(b-t,[0,2]);block(c-t,[1,2])
 x=block(d,[0]);y=block(d,[1]);bs[2]+=[u^v for u,v in zip(x,y)]
 for j in range(3):block(7-len(bs[j]),[j])
 assert pos<=14
 flats=[pts(z) for z in bs]
 if aff:flats[2]={z^x[0] for z in flats[2]}
 assert all(len(z)==128 for z in flats)
 return flats

def rank(bs):
 piv={}
 for b in bs:
  while b:
   j=b.bit_length()-1
   if j in piv:b^=piv[j]
   else:piv[j]=b;break
 return len(piv)

def verify(S,dirs,q,w):
 assert len(S)==w and rank(dirs)==7
 U=pts(dirs);assert len(U)==128
 reps={min(x^u for u in U) for x in S}
 assert len(reps)==q
 arr=np.zeros(16384,dtype=np.uint8);arr[list(S)]=1
 for i in range(14):
  a=arr.reshape(-1,1<<(i+1));a[:,1<<i:]^=a[:,:1<<i]
 deg=max((i.bit_count() for i in np.flatnonzero(arr)),default=-1)
 assert deg<=7
 return [w+128*k for k in range(129-q)]

ach={0,16384};tot=0
for w,(params,dirs,q) in pickle.load(open('central_triple_cert.pkl','rb')).items():
 fs=make(params);S=fs[0]^fs[1]^fs[2]
 for v in verify(S,dirs,q,w):ach|={v,16384-v}
 tot+=1
for w,(params,mask,val,dirs,q) in pickle.load(open('central_extra_cert.pkl','rb')).items():
 fs=make(params);S=fs[0]^fs[1]^fs[2]
 C={x^val for x in pts([1<<i for i in range(14) if not(mask>>i&1)])}
 assert len(C)==128
 for v in verify(S^C,dirs,q,w):ach|={v,16384-v}
 tot+=1
missing=[w for w in range(336,16049,2) if w not in ach]
print('Verified seeds:',tot)
print('Central-interval missing weights:',missing)
known={w for w in ach if 256<w<336}
print('Attained between 256 and 336:',sorted(known))
print('Unknown fringe list:',[w for w in range(258,336,2) if w not in known])
print('Projection bounds:',math.comb(334,2),2**16-1,math.comb(256,2),2**15-1)
