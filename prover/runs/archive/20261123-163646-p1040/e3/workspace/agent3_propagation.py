import json,os

def mul(p,q):
 out=set()
 for u in p:
  for v in q:
   if u and v and u[-1]==v[0]:continue
   w=u+v
   if w in out:out.remove(w)
   else:out.add(w)
 return out

def bracket(p,q):return mul(p,q)^mul(q,p)

def main():
 A={('A',)};B={('B',)};C={('C',)}
 gs=[B,A,A^B,C,A,A^C,C,B,B^C]
 def W(i,j,k,l):return bracket(bracket(bracket(gs[i],gs[j]),gs[k]),gs[l])
 p=W(0,1,5,2)
 expected={'ABAC','ABCA','ABCB','ACAB','ACBA','BABC','BACA','BACB','BCAB','BCBA','CABA','CBAB'}
 assert {''.join(w) for w in p}==expected
 witness=tuple('ABAC');checks=[]
 for c in range(4,31):
  assert witness in p and len(witness)==c
  checks.append({'c':c,'terms':len(p),'witness':''.join(witness)})
  x='B' if c%2==0 else 'C'
  assert witness[0]=='A' and x!=witness[-1]
  p=bracket(p,{(x,)})
  witness=witness+(x,)
 os.makedirs('workspace',exist_ok=True)
 with open('workspace/agent3_propagation_checks.json','w') as f:json.dump(checks,f,indent=2)
 print(json.dumps(checks,indent=2))

if __name__=='__main__':
 with open('workspace/agent3_propagation.py','w') as f:f.write(open(__file__).read())
 main()
