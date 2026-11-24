import sys,time
sys.path.insert(0,'workspace')
from agent2_upper_construction import witness,complete,subs,vertices
n=6;d=3;k=1;F=subs((1<<n)-1,d+1);M=len(F);checked=steps=0;start=time.time()
for mask in range(1,1<<M):
 fs=tuple(f for i,f in enumerate(F) if mask>>i&1)
 if witness(fs,k) is not None:
  extra=[1<<n];out=complete(fs,k,extra);state=set(fs)
  for f in out:
   assert f not in state
   state.add(f)
   assert witness(tuple(sorted(state)),k) is not None
  W=vertices(fs)|(1<<n)
  assert state==set(subs(W,d+1))
  checked+=1;steps+=len(out)
 if mask%1024==0:
  print(mask,'inputschecked',checked,'intermediates',steps,'seconds',round(time.time()-start,1),flush=True)
  witness.cache_clear()
print('EXHAUSTIVE UPPER COMPLETE',checked,steps,time.time()-start)
assert checked==18153
from pathlib import Path
Path('workspace/agent1_exhaustive_upper_check.py').write_text(Path('scratchpad.py').read_text())
