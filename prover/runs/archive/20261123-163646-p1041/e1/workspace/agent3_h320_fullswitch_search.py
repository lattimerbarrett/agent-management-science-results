import sys,itertools,time,json,numpy as np,random,collections,shutil
sys.path.insert(0,'workspace');import a1_cubic_closure_api as api
rng=random.Random(3883);N=8192;N12=4096;mons=[sum(1<<i for i in I) for d in range(6) for I in itertools.combinations(range(12),d)];pts=np.arange(4096,dtype=np.uint16);ev=np.empty((4096,len(mons)),dtype=np.uint8)
for j,m in enumerate(mons):ev[:,j]=((pts&m)==m)
cols=[int.from_bytes(r.tobytes(),'little') for r in np.packbits(ev,axis=1,bitorder='little')];del ev
rec=json.load(open('workspace/agent3_aperiodic_h320_three_affine.json'));h=int(rec['truth_hex'],16);pool=[h];seenW=set();sigrecs=[];stats=collections.Counter();hits={};start=time.time()
def signature(S):
 a=np.zeros(8192,dtype=np.int16);a[S]=1
 for i in range(13):
  st=1<<i;bl=a.reshape(-1,2*st);lo=bl[:,:st].copy();hi=bl[:,st:].copy();bl[:,:st]=lo+hi;bl[:,st:]=lo-hi
 va,ct=np.unique(np.abs(a),return_counts=True);return tuple(zip(map(int,va),map(int,ct)))
def kernel(S):
 p={};K=[]
 for j,x in enumerate(S):
  v=cols[x];c=1<<j
  while v:
   b=v.bit_length()-1
   if b not in p:p[b]=(v,c);break
   vv,cc=p[b];v^=vv;c^=cc
  if not v:K.append(c)
 return K
for step in range(5000):
 h=rng.choice(pool);S=np.array([x for x in range(N) if h>>x&1],dtype=np.uint16)
 for _ in range(40):
  dst,src=rng.sample(range(13),2);S^=((S>>src)&1)<<dst
 S^=rng.randrange(N);hb=sum(1<<int(x) for x in S);df=(hb&((1<<4096)-1))^(hb>>4096);DS=[x for x in range(4096) if df>>x&1];K=kernel(DS);stats[(len(DS),len(K))]+=1
 g=0
 for k in K:
  if rng.getrandbits(1):
   v=k
   while v:
    b=v&-v;g^=1<<DS[b.bit_length()-1];v^=b
 hh=hb^g^(g<<4096);assert hh.bit_count()==320;SS=[x for x in range(N) if hh>>x&1];sg=signature(SS)
 if sg not in seenW:
  seenW.add(sg);P=np.array(SS,dtype=np.uint16);corr=np.bincount((P[:,None]^P).ravel(),minlength=N);per=int(np.count_nonzero(corr==320));sigrecs.append({'truth_hex':hex(hh),'periodsize':per,'step':step,'derivative_weight':len(DS),'kernel_dim':len(K)});print('NEWORBITsignature',len(seenW),'periodsize',per,'DS',len(DS),'K',len(K),'step',step,flush=True)
  if per==1:
   E,kk,b5=api.closure_kernel(SS);print(' closure',len(E),'kernel',len(kk),'odd',any(v.bit_count()%2 for v in kk),flush=True)
   if any(v.bit_count()%2 for v in kk):
    if len(kk)>24:print('LARGEKERNEL',flush=True)
    else:
     tv=0
     for z in range(1,1<<len(kk)):
      tv^=kk[(z&-z).bit_length()-1]
      if tv.bit_count() not in (1,3,5,7):continue
      T=[x for j,x in enumerate(E) if tv>>j&1];rhs=0;inside=0
      for x in T:rhs^=api.cols[x]
      while rhs:
       b=rhs.bit_length()-1;vv,cc=b5[b];rhs^=vv;inside^=cc
      gg=sum(1<<x for j,x in enumerate(SS) if inside>>j&1)|sum(1<<x for x in T);F=gg|((gg^hh)<<8192);ww=F.bit_count();assert ww==320+2*len(T)
      arr=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
      for i in range(14):
       st=1<<i;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
      anf=list(map(int,np.flatnonzero(arr)));assert max(map(int.bit_count,anf))<=7
      hits[ww]={'truth_hex':hex(F),'anf':anf,'weight':ww};print('VERIFIED HIT',ww,flush=True);json.dump(hits,open('workspace/agent3_h320_fullswitch_hits.json','w'))
  pool.append(hh)
 elif rng.randrange(10)==0:
  if len(pool)>=100:pool.pop(rng.randrange(len(pool)))
  pool.append(hh)
 if step%200==0:print('step',step,'orbits',len(seenW),'pool',len(pool),'stats',dict(stats),'t',round(time.time()-start,1),flush=True);json.dump(sigrecs,open('workspace/agent3_h320_fullswitch_orbits.json','w'))
 if len(hits)==4 or time.time()-start>110:break
print('DONE',step,'orbits',len(seenW),'hits',list(hits),'stats',dict(stats),'t',time.time()-start,flush=True);json.dump(sigrecs,open('workspace/agent3_h320_fullswitch_orbits.json','w'));shutil.copyfile(__file__,'workspace/agent3_h320_fullswitch_search.py')
