import z3,json,time,itertools,math,functools
start=time.time()
@functools.lru_cache(None)
def triple_possible(k,n,A,B,C,T):
 card=[A,B,C]
 if T:
  if any(not a or T>a for a in card):return False
  a,b,c=[x.bit_length()-1 for x in card];t=T.bit_length()-1
  ex=[k-a-b+t,k-a-c+t,k-b-c+t]
  if min(ex)<0:return False
  return 3*k-a-b-c+t-min(ex)<=n
 opts=[[a.bit_length()] if a else list(range(k+1)) for a in card]
 for a,b,c in itertools.product(*opts):
  for t in range(min(a,b,c)+1):
   if any(v and d==t for v,d in zip(card,[a,b,c])):continue
   ex=[k+1-a-b+t,k+1-a-c+t,k+1-b-c+t]
   if min(ex)<0:continue
   for delta in range(min(ex)+1):
    if 3*(k+1)-a-b-c+t-delta>n+1:continue
    haspair=[bool(A or B),bool(A or C),bool(B or C)]
    need=sum(not hp and e==delta for hp,e in zip(haspair,ex))
    if need==0 or delta>=2 or delta==1 and need<=2:return True
 return False

def make_table(k,n):
 vals=[0]+[1<<j for j in range(k+1)];out=[]
 for a,b,c,t in itertools.product(vals,repeat=4):
  if t and (t>a or t>b or t>c):continue
  if triple_possible(k,n,a,b,c,t):out.append((a,b,c,t))
 return out
Told=make_table(4,8);Tnew=make_table(3,6);print('tables',len(Told),len(Tnew),'time',time.time()-start,flush=True);assert (4,1,4,0) not in Told
oldallowed=[16,24,28,30,32,34,36,38,40];newallowed=[8,12,14,16,18,20];s=z3.Solver();s.set(timeout=90000);ms=[z3.Int('m%d'%a) for a in range(1,8)];ns=[z3.Int('n%d'%a) for a in range(1,8)];ow=[];nw=[]
s.add(*[v>=0 for v in ms+ns],sum(ms)<=41,sum(ns)<=20)
for u in range(1,8):
 a=sum(ms[x-1] for x in range(1,8) if (u&x).bit_count()%2);b=sum(ns[x-1] for x in range(1,8) if (u&x).bit_count()%2);ow.append(a);nw.append(b);s.add(z3.Or(*[a==w for w in oldallowed]),z3.Or(*[b==w for w in newallowed]))
s.add(ow[0]==16,z3.Or(*[b==8 for b in nw]));s.add(sum(sum(z3.If(ow[a]==w,w*ns[a],0) for w in oldallowed) for a in range(7))==330)
for counts,ws,minw,table in [(ms,ow,16,Told),(ns,nw,8,Tnew)]:
 for u,v,w in itertools.combinations(range(1,8),3):
  if u^v^w==0:continue
  pair=lambda a,b:sum(counts[x-1] for x in range(1,8) if (a&x).bit_count()%2 and (b&x).bit_count()%2)
  pa,pb,pc=pair(u,v),pair(u,w),pair(v,w);tri=sum(counts[x-1] for x in range(1,8) if all((y&x).bit_count()%2 for y in [u,v,w]))
  s.add(z3.Implies(z3.And(ws[u-1]==minw,ws[v-1]==minw,ws[w-1]==minw),z3.Or(*[z3.And(pa==a,pb==b,pc==c,tri==t) for a,b,c,t in table])))
print('built',time.time()-start,flush=True);ret=s.check();print('RESULT',ret,'time',time.time()-start,flush=True)
if ret==z3.sat:
 m=s.model();r={'old_counts':[m.eval(v).as_long() for v in ms],'new_counts':[m.eval(v).as_long() for v in ns],'old_weights':[m.eval(v).as_long() for v in ow],'new_weights':[m.eval(v).as_long() for v in nw]};print(r);json.dump(r,open('workspace/agent3_rank3_334_profile.json','w'))
for target in [322,326,330,334]:
 rr=z3.Solver();a=[z3.Int('aa%d'%x) for x in range(1,4)];b=[z3.Int('bb%d'%x) for x in range(1,4)];rr.add(*[x>=0 for x in a+b],sum(a)<=41,sum(b)<=20);ww=[]
 for u in range(1,4):
  w=sum(a[x-1] for x in range(1,4) if (u&x).bit_count()%2);v=sum(b[x-1] for x in range(1,4) if (u&x).bit_count()%2);ww.append(w);rr.add(z3.Or(*[w==v for v in oldallowed]),z3.Or(*[v==x for x in newallowed]))
 rr.add(sum(sum(z3.If(ww[j]==v,v*b[j],0) for v in oldallowed) for j in range(3))==target);print('rank2',target,rr.check(),flush=True)
import shutil;shutil.copyfile(__file__,'workspace/agent3_rank3_tensor_profile_model.py')
