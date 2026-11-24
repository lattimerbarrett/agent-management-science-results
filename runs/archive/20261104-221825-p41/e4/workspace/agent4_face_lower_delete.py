"""Codimension-one pure skeleton of an arbitrary nonempty-face deletion."""
from agent3_checker import subsets,deletion_link,verify
from agent2_vertex_completion import full_certificate
from agent4_lower_delete import cone_certificate

def lower_face_delete_certificate(fs,k,c,S):
 assert S
 fs=tuple(sorted(fs));r=fs[0].bit_count();assert r>=1
 def rec(fs,c,S):
  r=fs[0].bit_count()
  if c[0]=='simplex':
   W=c[1]
   if W&S!=S:return full_certificate(W,r-1)
   return cone_certificate(full_certificate(S,S.bit_count()-1),W^S)
  _,s,dc,lc=c;D,L=deletion_link(fs,s)
  if S&s==S or s.bit_count()==r:return rec(D,dc,S)
  return ('shed',s,rec(D,dc,S),rec(L,lc,S&~s))
 target=tuple(sorted({g for F in fs for g in subsets(F,r-1) if g&S!=S}))
 out=rec(fs,c,S);verify(target,k,out)
 return target,out
