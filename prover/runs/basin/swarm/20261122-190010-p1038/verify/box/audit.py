import sys, time
sys.path.insert(0, 'agents/agent_1')
import scratchpad as s
from sage.all import QQ
st=time.time()
s.check_constants()
s.check_division_identity()
for r in [QQ(1)/4,QQ(1)]:
    full=s.direct_m1(64,32,r=r)
    red=s.reduced(1,64,32,r=r,eps=QQ(1)/1000000,bits=2048)[0]
    print('m=1 full and reduced:',r,s.certified_sign(full),s.certified_sign(red),'ratio=',full/red,flush=True)
for m in [2,3,5]:
    vals=s.reduced(m,64*m,32*m,r=QQ(1),eps=QQ(1)/1000000,bits=1024)
    vals2=s.reduced(m,64*m,32*m,r=QQ(1)/128,eps=QQ(1)/1000000,bits=1024)
    print('m=',m,'endpoint signs=',list(map(s.certified_sign, vals)),list(map(s.certified_sign,vals2)),flush=True)
print('time',time.time()-st)
