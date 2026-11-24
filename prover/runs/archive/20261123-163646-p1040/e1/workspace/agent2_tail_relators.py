"""Exact partial-inner / conjugated-tail relations in IA3."""
import json
from pathlib import Path
from itertools import product
from sage.all import Matrix,ZZ
from agent1_degree3 import G,expand,compose,inv,red
from agent1_degree3_closure import initial_vector

def comm(a,b):return red(a+b+inv(a)+inv(b))
def generate():
 d=json.load(open('workspace/agent2_nielsen_actions_n3.json'));idx={tuple(nm):i+1 for i,nm in enumerate(d['names'])}
 gi=[tuple(map(tuple,g)) for g in d['inverses']];ident=((1,),(2,),(3,))
 def evaluate(w):
  f=ident
  for x in w:f=compose(f,G[x-1] if x>0 else gi[-x-1])
  return f
 rel=[];vectors=[]
 for i in range(3):
  j,k=[x for x in range(3) if x!=i]
  C=(idx['C',i,j,k],);Pj=(idx['K',k,j],);Pk=(idx['K',j,k],);Pu=comm(Pj,Pk)
  for a,b in product(range(-2,3),repeat=2):
   pw=(Pj*a if a>=0 else inv(Pj)*(-a))+(Pk*b if b>=0 else inv(Pk)*(-b))
   Tv=red(pw+C+inv(pw));r=red(comm(C,Tv)+inv(comm(Pu,Tv)))
   assert evaluate(r)==ident,(i,a,b,r)
   rel.append(r);vectors.append(initial_vector(expand(r)))
 Path('workspace/agent2_tail_relator_words.json').write_text(json.dumps(rel))
 Path('workspace/agent2_tail_relator_vectors.json').write_text(json.dumps([[int(x) for x in v] for v in vectors]))
 print('exacttailrelators',len(rel),'rank',Matrix(ZZ,vectors).rank())
 return rel,vectors
if __name__=='__main__':generate()
