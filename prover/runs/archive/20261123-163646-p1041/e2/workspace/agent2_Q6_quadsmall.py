import sys,json,pathlib,itertools,collections,time
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese
q=lambda x: ((x&1)*(x>>1&1))^((x>>2&1)*(x>>3&1))^((x>>4&1)*(x>>5&1))
Q=[x for x in range(64) if not q(x)];mons=[sum(1<<i for i in J) for d in range(3) for J in itertools.combinations(range(6),d)]
B={};basis=[]
for mon in mons:
 r=sum(1<<i for i,p in enumerate(Q) if p&mon==mon);full=sum(1<<p for p in range(64) if p&mon==mon)
 while r:
  k=r.bit_length()-1
  if k not in B:B[k]=(r,full);basis.append((r,full));break
  r^=B[k][0];full^=B[k][1]
assert len(basis)==21
z=f=0;hist=collections.Counter();small=[];t=time.time()
for i in range(1<<21):
 if i:
  k=(i&-i).bit_length()-1;z^=basis[k][0];f^=basis[k][1]
 w=z.bit_count();hist[w]+=1
 if 0<w<=8:small.append({'weight':w,'Qmask':z,'full':f})
print('hist',hist,'small',len(small),'sec',time.time()-t)
# rank3 restriction
BB={}
for mon in [sum(1<<i for i in J) for d in range(4) for J in itertools.combinations(range(6),d)]:
 z=sum(1<<i for i,p in enumerate(Q) if p&mon==mon);f=sum(1<<p for p in range(64) if p&mon==mon)
 while z:
  k=z.bit_length()-1
  if k not in BB:BB[k]=(z,f);break
  z^=BB[k][0];f^=BB[k][1]
print('rank3',len(BB));assert len(BB)==35 and min(hist.keys()-{0})==6
json.dump({'Q':Q,'weight_enumerator':dict(hist),'small':small,'cubic_extension':{str(k):v for k,v in BB.items()}},open('workspace/agent2_Q6_quadsmall.json','w'));pathlib.Path('workspace/agent2_Q6_quadsmall.py').write_text(pathlib.Path(__file__).read_text())
