import sys,json,pathlib,itertools,collections
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese

def kernel(S,vs):
 B={};out=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out
D=json.load(open('workspace/agent2_Q6_quadsmall.json'));Q=D['Q'];BB={int(k):tuple(v) for k,v in D['cubic_extension'].items()}
q=lambda x: ((x&1)*(x>>1&1))^((x>>2&1)*(x>>3&1))^((x>>4&1)*(x>>5&1))
qf=sum(q(z)<<z for z in range(64));v2=veronese(7,2)
for I in itertools.combinations(range(36),4):
 z=sum(1<<i for i in I);hf=0
 while z:
  k=z.bit_length()-1;z^=BB[k][0];hf^=BB[k][1]
 sf=hf|((hf^qf)<<64);C=[z for z in range(128) if sf>>z&1];K=kernel(C,v2)
 if len(K)==11:break
T=[z|(r<<7) for z in C for r in range(8)];assert len(T)==288
KT=kernel(T,veronese(10,5));assert len(KT)==14
json.dump({'I':I,'C':C,'T':T,'K':KT},open('workspace/agent2_T28810_K14_seed.json','w'));print('I',I,'C',C,'Kdims',len(K),len(KT));pathlib.Path('workspace/agent2_T28810_K14_seed.py').write_text(pathlib.Path(__file__).read_text())
