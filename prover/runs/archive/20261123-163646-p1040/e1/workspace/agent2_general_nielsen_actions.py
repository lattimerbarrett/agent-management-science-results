"""Exact all-rank Magnus-word conjugation formulas, checked as free automorphisms."""
import json
from pathlib import Path
from agent2_nielsen_actions import magnus
from degree2_certificate import compose,red

def actions(n):
 assert n>=3
 data3=json.loads(Path('workspace/agent2_nielsen_actions_n3.json').read_text())
 id3,g3,gi3,names3=magnus(3)
 ident,gs,gis,names=magnus(n);index={tuple(v):i+1 for i,v in enumerate(names)}
 def coordinate(typ,i,j,k=None):
  if typ=='K':return index[('K',i,j)]
  if j<k:return index[('C',i,j,k)]
  return -index[('C',i,k,j)]
 def lift(w,labels):
  out=[]
  for x in w:
   nm=names3[abs(x)-1]
   if nm[0]=='K':y=coordinate('K',labels[nm[1]],labels[nm[2]])
   else:y=coordinate('C',labels[nm[1]],labels[nm[2]],labels[nm[3]])
   out.append(y if x>0 else -y)
  return tuple(out)
 def evaluate(w):
  f=ident
  for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
  return f
 acts={}
 # T sends x0 -> x0*x1.
 t=list(ident);ti=list(ident);t[0]=(1,2);ti[0]=(1,-2);words=[]
 for num,nm in enumerate(names,1):
  support=set(nm[1:]);union=support|{0,1}
  if len(union)<=3:
   extra=next((x for x in union if x not in (0,1)),next(x for x in range(n) if x not in (0,1)))
   labels=[0,1,extra];back={v:i for i,v in enumerate(labels)}
   if nm[0]=='K':idx3=next(i for i,v in enumerate(names3) if v==('K',back[nm[1]],back[nm[2]]));sgn=1
   else:
    a,b=back[nm[2]],back[nm[3]];sgn=1 if a<b else -1
    idx3=next(i for i,v in enumerate(names3) if v==('C',back[nm[1]],min(a,b),max(a,b)))
   w=lift(data3['actions']['T']['words'][idx3],labels)
   if sgn<0:w=tuple(-x for x in reversed(w))
  elif nm[0]=='K' or 0 not in support and 1 not in support:
   w=(num,)
  else:
   _,i,j,k=nm
   if i==0:
    z=coordinate('K',0,1);w=(-z,num,z)
   elif i==1:
    z=coordinate('K',0,1);c=coordinate('C',0,j,k);w=(-z,-c,z,num)
   elif j==0:
    z=coordinate('K',i,0);c=coordinate('C',i,1,k);w=(-z,c,z,num)
   else:w=(num,)
  assert evaluate(w)==compose(t,compose(gs[num-1],ti)),('T',n,nm,w)
  words.append(w)
 acts['T']={'auto':t,'inverse':ti,'words':words}
 # I inverts x0; use embedded checked rank3 formulas.
 t=list(ident);t[0]=(-1,);words=[]
 for num,nm in enumerate(names,1):
  support=set(nm[1:])
  if 0 not in support:w=(num,)
  else:
   rest=sorted(support-{0});labels=[0]+rest
   labels += [x for x in range(n) if x not in labels][:3-len(labels)]
   back={v:i for i,v in enumerate(labels)}
   if nm[0]=='K':idx3=next(i for i,v in enumerate(names3) if v==('K',back[nm[1]],back[nm[2]]));sgn=1
   else:
    a,b=back[nm[2]],back[nm[3]];sgn=1 if a<b else -1
    idx3=next(i for i,v in enumerate(names3) if v==('C',back[nm[1]],min(a,b),max(a,b)))
   w=lift(data3['actions']['I']['words'][idx3],labels)
   if sgn<0:w=tuple(-x for x in reversed(w))
  assert evaluate(w)==compose(t,compose(gs[num-1],t)),('I',n,nm,w)
  words.append(w)
 acts['I']={'auto':t,'inverse':t,'words':words}
 for key,perm in [('P',[1,0]+list(range(2,n))),('C',[(i+1)%n for i in range(n)])]:
  t=tuple((perm[i]+1,) for i in range(n));pinv=[perm.index(i) for i in range(n)];ti=tuple((pinv[i]+1,) for i in range(n));words=[]
  for num,nm in enumerate(names,1):
   y=coordinate(nm[0],*[perm[i] for i in nm[1:]]);w=(y,)
   assert evaluate(w)==compose(t,compose(gs[num-1],ti)),(key,n,nm,w)
   words.append(w)
  acts[key]={'auto':t,'inverse':ti,'words':words}
 result={'n':n,'generators':gs,'inverses':gis,'names':names,'actions':acts}
 Path('workspace/agent2_nielsen_actions_n%d.json'%n).write_text(json.dumps(result))
 print('rank',n,'checked',4*len(gs),'exact conjugation expressions')
 return result
if __name__=='__main__':
 for n in range(3,9):actions(n)
