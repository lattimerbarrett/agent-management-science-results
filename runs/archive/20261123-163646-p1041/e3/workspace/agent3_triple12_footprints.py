"""Canonical full-span12 arrangements of three affine7-flats, footprint bounds.
The finite enumeration uses the standard three-subspace/D4 decomposition:
common,pair-only,single-only atoms plus2D blocks carrying three distinctlines.
Does NOT assert arbitrary KTA words have such a three-flat representation.
"""
import itertools,json
N=1<<12;F=N-1

def span(vs):
 s={0}
 for v in vs:s|={x^v for x in s}
 return s

def rankbasis(rows):
 P={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j in P:v^=P[j]
   else:P[j]=v;break
 return P

def footprints(Union):
 mons=sorted(range(N),key=lambda x:(x.bit_count(),x));ix={x:i for i,x in enumerate(mons)}
 rows=[]
 for x in Union:
  a=F^x;t=x;v=0
  while True:
   v^=1<<ix[a|t]
   if not t:break
   t=(t-1)&x
  rows.append(v)
 P=rankbasis(rows);assert len(P)==len(Union)
 bad={mons[j] for j in P}
 assert all((m|1<<i) in bad for m in bad for i in range(12))
 counts=[int(m not in bad) for m in range(N)]
 for i in range(12):
  for m in range(N):
   if not m>>i&1:counts[m]+=counts[m|1<<i]
 return [min(counts[m] for m in range(N) if m not in bad and m.bit_count()<=d) for d in (6,7)]

def arrangements():
 for a in range(8):
  for b,c,d in itertools.product(range(8),repeat=3):
   for h in range(8):
    e=7-a-b-c-h;f=7-a-b-d-h;g=7-a-c-d-h
    if min(e,f,g)<0 or a+b+c+d+e+f+g+2*h!=12:continue
    for kind in ['lin','cycle','path']:
     if kind!='path' and not b>=c>=d:continue
     if kind=='cycle' and not h:continue
     if kind=='path' and (not e or b<c):continue
     p=1<<(a+b);q=1<<(a+c);r=0 if kind=='path' else 1<<(a+d);t=1<<a if kind=='lin' else 0
     w=384-2*(p+q+r)+4*t
     if w not in [288,296,304,308,312]:continue
     bases=[[],[],[]];k=0;singleU=[];tri=[]
     for size,inds in [(a,[0,1,2]),(b,[0,1]),(c,[0,2]),(d,[1,2]),(e,[0]),(f,[1]),(g,[2])]:
      for _ in range(size):
       v=1<<k;k+=1
       for j in inds:bases[j].append(v)
       if inds==[0]:singleU.append(v)
     for _ in range(h):
      v=1<<k;u=1<<(k+1);k+=2
      bases[0].append(v);bases[1].append(u);bases[2].append(v^u);tri.append(v)
     assert k==12 and all(len(v)==7 for v in bases)
     S=[span(B) for B in bases]
     offset=0 if kind=='lin' else tri[0] if kind=='cycle' else singleU[0]
     S[2]={v^offset for v in S[2]}
     assert len(S[0]^S[1]^S[2])==w
     assert [len(S[0]&S[1]),len(S[0]&S[2]),len(S[1]&S[2]),len(S[0]&S[1]&S[2])]==[p,q,r,t]
     assert len(span([v for B in bases for v in B]))==N
     yield dict(kind=kind,atoms=[a,b,c,d,e,f,g,h],weight=w,bases=bases,offset=offset),S

def verify():
 out=[]
 for A,S in arrangements():
  U=S[0]|S[1]|S[2]
  fp=footprints(U)
  A.update(union=len(U),footprints67=fp)
  out.append(A)
  print(A['kind'],A['atoms'],'g',A['weight'],'union',len(U),'footprint67',fp)
 assert len(out)==22
 from pathlib import Path
 Path('workspace/agent3_triple12_footprints.json').write_text(json.dumps(out,indent=2))
 print('Verified all22 canonical triple-flat arrangements; no arbitrary-word classification assumed.')
if __name__=='__main__':verify()
