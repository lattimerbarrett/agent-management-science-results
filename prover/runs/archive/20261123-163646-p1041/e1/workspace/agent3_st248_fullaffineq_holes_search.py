import sys,time,random,itertools,numpy as np,json,collections,shutil
shutil.copyfile(__file__,'workspace/agent3_st248_fullaffineq_holes_search.py')
sys.path.insert(0,'workspace');import agent4_st248_outside_api as api
rng=random.Random(78924);H=api.H;HS=set(H);J=set(range(4));A=list(range(128));B=[r+(b<<7) for b in range(32) for r in range(4)];HP={x:i for i,x in enumerate(H)};MASK=(1<<248)-1
start=time.time();targets={322,326,330,334};hits={}
def span(bs,s=0):
 out=[s]
 for b in bs:out += [x^b for x in out]
 return out
def bm(S):return sum(1<<x for x in S)
def rank(bs):
 p={}
 for v in bs:
  while v:
   b=v.bit_length()-1
   if b not in p:p[b]=v;break
   v^=p[b]
 return len(p)
def image_joint(P):
 bas={}
 for x in P-HS-J:
  v=api.cols[x]
  while v:
   b=v.bit_length()-1
   if b not in bas:bas[b]=(v,0);break
   v^=bas[b][0]
 eb={};gens=[]
 for j,x in enumerate(H+sorted(J)):
  v=api.cols[x];im=1<<j
  while v:
   b=v.bit_length()-1
   if b not in bas:bas[b]=(v,im);break
   vv,ii=bas[b];v^=vv;im^=ii
  if v:continue
  for b in api.qp:
   if im>>b&1:im^=api.qb[b]
  if api.insert(eb,im):gens.append(im)
 return gens
# all q=deltaA*LA+deltaB*LB with arbitrary affine LA/LB; force q|J=1
Afamily=[];Bfamily=[]
for family,flat in ((Afamily,A),(Bfamily,B)):
 for code in range(256):family.append({x for i,x in enumerate(flat) if ((code>>1)&i).bit_count()%2^(code&1)})
BbyJ={}
for Q in Bfamily:BbyJ.setdefault(bm(Q&J),[]).append(Q)
def recover_g(P,Hword,Jword):
 supp=[x for j,x in enumerate(H) if Hword>>j&1]+[x for j,x in enumerate(sorted(J)) if Jword>>j&1]
 rhs=0;gt=bm(supp)
 for x in supp:rhs^=api.cols[x]
 piv={}
 for x in P-HS-J:
  v=api.cols[x];u=1<<x
  while v:
   b=v.bit_length()-1
   if b not in piv:piv[b]=(v,u);break
   vv,uu=piv[b];v^=vv;u^=uu
 while rhs:
  b=rhs.bit_length()-1;assert b in piv
  vv,uu=piv[b];rhs^=vv;gt^=uu
 return gt
for trial in range(30):
 # p = affine5-flat in A, extended by one general direction
 bs=[rng.randrange(1,128) for _ in range(5)]
 if rank(bs)<5:continue
 z=rng.randrange(128,4096);P=set(span(bs+[z],rng.randrange(128)));assert len(P)==64
 outside=len(P-HS)
 if not 22<=outside<=43:continue
 gens=image_joint(P)
 if len(gens)>16:continue
 qclasses={}
 for QA in Afamily:
  for QB in BbyJ[15^bm(QA&J)]:
   Q=QA^QB;N=sum(1<<HP[x] for x in P&Q&HS);tail=0
   qclasses.setdefault((N,tail),Q)
 im=0;decodes=0;cache={}
 for zz in range(1<<len(gens)):
  if zz:im^=gens[(zz&-zz).bit_length()-1]
  ih=im&MASK;jword=im>>248
  for (N,tail),Q in qclasses.items():
   extra=(jword&tail).bit_count();need={t:(t-248)//2-outside-2*extra for t in targets}
   if not any(0<=v<=15 for v in need.values()):continue
   inp=N^ih
   if inp not in cache:cache[inp]=api.decode(inp);decodes+=1
   err=cache[inp]
   if err is None:continue
   w=248+2*outside+2*err.bit_count()+4*extra
   if w not in targets:continue
   g=recover_g(P,N^err,jword);p=bm(P);q=bm(Q);h=bm(HS)
   F=g|((g^p)<<4096)|((g^q)<<8192)|((g^p^q^h)<<12288);assert F.bit_count()==w
   a=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for bit in range(14):
    st=1<<bit;bl=a.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(a)));assert max(map(int.bit_count,anf))<=7
   print('FOUND',w,'trial',trial,flush=True);hits[w]={'truth_hex':hex(F),'anf':anf};json.dump(hits,open('workspace/agent3_st248_hole_hits.json','w'));targets.remove(w)
  if not targets:break
 if trial%10==0:print('trial',trial,'outside',outside,'extras',len(gens),'qclasses',len(qclasses),'decodes',decodes,'cache',len(cache),'time',round(time.time()-start,2),flush=True)
 if not targets:break
print('DONE remain',targets,'time',time.time()-start,flush=True)
import shutil;shutil.copyfile(__file__,'workspace/agent3_st248_fullaffineq_holes_search.py')
