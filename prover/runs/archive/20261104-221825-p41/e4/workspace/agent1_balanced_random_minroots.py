import sys,json,random,time
sys.path.insert(0,'workspace')
import agent4_minroots as mr
from agent2_fastcheck import fast_homology_certificate
from agent3_checker import subsets,deletion_link,verify
from agent4_factor_completion import factor_data
mr.certificate=fast_homology_certificate
p=json.load(open('workspace/agent2_balanced_min_tree_stress.json'));fs=tuple(p['facets'])
full=tuple(sorted(subsets(511,3)))
random.seed(2471)
count=0;start=time.monotonic()
def walk(fs,T):
 global count
 if len(fs)==1:
  # factor_data returns either block metadata; inspect separately if needed.
  count+=1
  return ('simplex',fs[0]),[(fs,T)]
 s=random.choice(mr.roots(fs,1));de,li=deletion_link(fs,s);dt,lt=deletion_link(T,s)
 assert all(f.bit_count()==T[0].bit_count() for f in dt)
 dc,a=walk(de,dt);lc,b=walk(li,lt)
 return ('shed',s,dc,lc),a+b
for trial in range(1000):
 c,leaves=walk(fs,full);verify(fs,1,c)
 for f,T in leaves:
  rank=T[0].bit_count()
  fd=factor_data(T)
  assert fd[2]>=rank,(trial,f,T,fd)
 if trial%100==0:print('trial',trial,'leaves',count,'states',mr.roots.cache_info().currsize,'seconds',time.monotonic()-start,flush=True)
