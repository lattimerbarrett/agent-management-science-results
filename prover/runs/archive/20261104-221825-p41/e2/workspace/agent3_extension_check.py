import itertools,sys,json
sys.path.insert(0,'workspace')
from agent4_checker import dec

def submasks(s):
 t=s
 while True:
  yield t
  if not t: break
  t=(t-1)&s

def faces_of(facets):
 return {g for f in facets for g in submasks(f)}

def appendable(facets,f):
 old=faces_of(facets)
 ridges=[f^(1<<i) for i in range(f.bit_length()) if f>>i&1 and (f^(1<<i)) in old]
 return bool(ridges) and all(any(g&r==g for r in ridges) for g in submasks(f) if g in old)

def bad_link_witness(facets,f):
 old=faces_of(facets)
 inter=[g for g in submasks(f) if g in old]
 maxs=[g for g in inter if not any(g!=h and g&h==g for h in inter)]
 for g in maxs:
  if g.bit_count()<f.bit_count()-1:
   left={i for b in facets if b&g==g for i in range(b.bit_length()) if (b^g)>>i&1}
   right={i for i in range(f.bit_length()) if (f^g)>>i&1}
   assert left and right and left.isdisjoint(right)
   return g,sorted(left),sorted(right)
 return None

def verify(n,d):
 fs=[sum(1<<x for x in c) for c in itertools.combinations(range(n),d+1)]
 good=bad=0
 for bits in range(1,1<<len(fs)):
  facets=tuple(f for i,f in enumerate(fs) if bits>>i&1)
  if not dec(facets,d):continue
  for f in fs:
   if f in facets:continue
   app=appendable(facets,f)
   new=dec(tuple(sorted(facets+(f,))),d)
   assert app==new,(facets,f,app,new)
   if app:good+=1
   else:
    assert bad_link_witness(facets,f) is not None
    bad+=1
 return {'n':n,'d':d,'appendable_tests':good,'bad_link_witness_tests':bad}
if __name__=='__main__':
 print(verify(5,2))
 print(verify(6,3))
 with open('scratchpad.py') as src, open('workspace/agent3_extension_check.py','w') as dst: dst.write(src.read())
