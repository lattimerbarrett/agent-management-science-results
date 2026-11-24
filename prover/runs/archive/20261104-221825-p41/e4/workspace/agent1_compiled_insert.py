import sys,json,time
sys.path.insert(0,'workspace')
from agent3_checker import certificate,deletion_link,subsets
from agent1_shellability import faces
p=json.load(open('workspace/agent3_nonvertex_example.json'))
fs=tuple(sorted(p['facets']));c=certificate(fs,1)

def shift_cert(c,offset):
 if c[0]=='simplex':return ('simplex',c[1]<<offset)
 return ('shed',c[1]<<offset,shift_cert(c[2],offset),shift_cert(c[3],offset))
def join_cert(c1,c2):
 if c1[0]=='simplex':
  W=c1[1]
  if c2[0]=='simplex':return ('simplex',W|c2[1])
  return ('shed',c2[1],join_cert(c1,c2[2]),join_cert(c1,c2[3]))
 return ('shed',c1[1],join_cert(c1[2],c2),join_cert(c1[3],c2))

def compile_tree(fs,c):
 if c[0]=='simplex':return c
 _,s,dc,lc=c
 de,li=deletion_link(fs,s)
 return ('shed',s,frozenset(faces(de)),compile_tree(de,dc),compile_tree(li,lc))
def permits(t,F):
 if t[0]=='simplex':return (t[1]&F).bit_count()==t[1].bit_count()-1
 _,s,d,dc,lc=t
 if F&s==s:
  return all((F^v) in d for v in subsets(s,1)) and permits(lc,F^s)
 return permits(dc,F)

