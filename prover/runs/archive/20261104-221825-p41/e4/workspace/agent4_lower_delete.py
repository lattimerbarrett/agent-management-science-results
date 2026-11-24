"""Explicit certificate transforms for lower skeletons of arbitrary vertex deletions."""
from agent3_checker import subsets,deletion_link,verify
from agent2_vertex_completion import full_certificate
from agent2_boundary_fill import fill_boundary

def lower_delete_facets(fs,v):
 r=fs[0].bit_count();assert r>=1 and v.bit_count()==1
 return tuple(sorted({s for F in fs for s in subsets(F,r-1) if not s&v}))

def lower_delete_certificate(fs,k,c,v):
 fs=tuple(sorted(fs));r=fs[0].bit_count();assert r>=1
 def rec(fs,c):
  r=fs[0].bit_count()
  if c[0]=='simplex':
   W=c[1]
   return ('simplex',W^v) if W&v else full_certificate(W,r-1)
  _,s,dc,lc=c;D,L=deletion_link(fs,s)
  if s&v or s.bit_count()==r:return rec(D,dc)
  return ('shed',s,rec(D,dc),rec(L,lc))
 out=rec(fs,c);target=lower_delete_facets(fs,v)
 verify(target,k,out)
 return target,out

def cone_certificate(c,v):
 if c[0]=='simplex':return ('simplex',c[1]|v)
 return ('shed',c[1],cone_certificate(c[2],v),cone_certificate(c[3],v))

def cone_shadow_certificate(fs,k,c,v):
 fs=tuple(sorted(fs));K,kc=lower_delete_certificate(fs,k,c,v)
 cur=tuple(sorted(v|F for F in K));out=cone_certificate(kc,v)
 verify(cur,k,out)
 for F in fs:
  if not F&v:
   out=fill_boundary(cur,k,out,F);cur=tuple(sorted(cur+(F,)))
 target=tuple(sorted(set(fs)|{v|F for F in K}))
 assert cur==target
 verify(target,k,out)
 return target,out
