import sys,random,itertools,time,json,pathlib
sys.path.insert(0,'workspace')
from agent3_check import *
from agent4_fastcert import fastcert
from agent1_filling import check_certificate
from agent2_dim3_upper import prefix_order

def dl(F,s):return tuple(f for f in F if f&s!=s)
def li(F,s):return tuple(sorted(f^s for f in F if f&s==s))
def linkcert(F,c,u):
 if c[0]=='simplex':return ('simplex',F[0]^u)
 _,s,dc,lc=c;D=dl(F,s);L=li(F,s)
 if s==u:return lc
 d=linkcert(D,dc,u)
 if s&u:return ('shed',s^u,d,lc)
 if not any(f&u for f in L):return d
 return ('shed',s,d,linkcert(L,lc,u))
def skel(F):return tuple(sorted({f^(1<<v) for f in F for v in range(f.bit_length()) if f>>v&1}))
def skelcert(F,c):
 r=F[0].bit_count()
 if r==1:return ('simplex',0)
 if c[0]=='simplex':return k_certificate(skel(F),0)
 _,s,dc,lc=c;D=dl(F,s);L=li(F,s)
 if s.bit_count()==r:return skelcert(D,dc)
 return ('shed',s,skelcert(D,dc),skelcert(L,lc))

random.seed(8241)
for q in [4,5,6]:
 for trial in range(100):
  F=((1<<q)-1,);c=('simplex',F[0])
  for n in range(q,q+7):
   u=1<<random.randrange(n);v=1<<n
   M=li(F,u);mc=linkcert(F,c,u)
   H=skel(M);hc=skelcert(M,mc)
   order=prefix_order(H,1,hc);count=random.randint(1,len(order))
   L=tuple(sorted(h for h,cc in order[:count]));lc=order[count-1][1]
   clone=tuple(sorted(F+tuple(v|f for f in M)));cc=('shed',v,c,mc)
   F=tuple(sorted(clone+tuple(u|v|f for f in L)));c=('shed',u|v,cc,lc)
   if trial<2:assert check_certificate(F,1,c)
  G=skel(F);t=time.time();vc=fastcert(G,0)
  if vc is None:
   print('COUNTEREX',q,trial,len(F),len(G),flush=True)
   json.dump({'F':F,'G':G,'cert':c},open('workspace/agent2_skeleton_reduction_counter.json','w'));raise SystemExit
  if trial%10==0:print('passed',q,trial,'n',q+7,'F',len(F),'G',len(G),'VDsec',round(time.time()-t,2),flush=True)
  if trial%10==0:fastcert.cache_clear()
pathlib.Path('workspace/agent2_clone_thicken_search.py').write_text(pathlib.Path(__file__).read_text())
