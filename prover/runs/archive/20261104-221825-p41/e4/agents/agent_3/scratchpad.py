import sys,json,itertools,random,time
sys.path.insert(0,'workspace')
from agent3_checker import *
from agent3_tree_capacity_completion import normalize,facets,score

def uniform_order(W,U,r):
 if r==0:return ()
 out=[];current=W
 for v in subsets(U&~W,1):
  T=next(subsets(current,r-1));out.append(v|T)
  out.extend(v|f for f in uniform_order(T,current,r-1));current|=v
 return tuple(out)
def cap_order(U,N,r,W):
 U,N=normalize(U,N,r);assert score(U,N,r)>=r
 if not N:return uniform_order(W,U,r)
 v=next(subsets(N[0]&~W,1));nd=tuple(n for n in N if not n&v);nl=tuple(n&~v for n in N);S=facets(U^v,nl,r-1)[0]
 return cap_order(U^v,nd,r,W)+(v|S,)+tuple(v|g for g in cap_order(U^v,nl,r-1,S))
def tree_order(c,U,N,r):
 U,N=normalize(U,N,r)
 if c[0]=='simplex':return cap_order(U,N,r,c[1])
 s=c[1]
 return tree_order(c[2],U,tuple(N)+(s,),r)+tuple(s|g for g in tree_order(c[3],U&~s,tuple(n&~s for n in N),r-s.bit_count()))
def app(fb,f):
 R=sum(v for v in subsets(f,1) if fb>>(f^v)&1)
 return not(fb>>R&1)
x=json.load(open('workspace/agent3_k2_not_k1.json'));fs=tuple(x['facets']);r=6;U=(1<<14)-1;A=15<<14;c=x['cert'];O=tree_order(c,U|A,(),r);pairs=[(F&U,F>>14) for F in O]
basefb=0
for f in fs:
 for g in subsets(f):basefb|=1<<g
maps=list(itertools.product(tuple(subsets(U,1)),repeat=4));random.Random(731).shuffle(maps)
t=__import__('time').time()
for i,vals in enumerate(maps):
 images=[0]*16
 for s in range(1,16):
  z=s&-s;images[s]=images[s^z]|vals[z.bit_length()-1]
 fb=basefb;cur=set(fs);proj=[]
 for old,ghost in pairs:
  f=old|images[ghost]
  if f.bit_count()!=6 or f in cur:continue
  if not app(fb,f):break
  cur.add(f);proj.append(f)
  for g in subsets(f):fb|=1<<g
 else:
  print('GOODMAP',vals,'steps',len(proj),'tested',i+1,'time',__import__('time').time()-t,flush=True)
  json.dump({'map':vals,'order':proj},open('workspace/agent3_fold_general_good.json','w'));break
 if i%5000==0:print('tried',i,'time',__import__('time').time()-t,flush=True)
else:print('ALL',len(maps),'MAPS FAIL',__import__('time').time()-t,flush=True)
