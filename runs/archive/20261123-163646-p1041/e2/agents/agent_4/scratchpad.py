from pathlib import Path
base=Path('workspace/agent4_higherorthogonal320_pipeline.py').read_text();exec(base[:base.index("\nD=json.loads")]);s=Path('workspace/agent4_indecomp160_Grassmann.py').read_text()
# Reuse affsolve/extend2/key definitions without prior run.
s2=s[s.index('def affsolve'):s.index('start=time.time()')];exec(s2)
import json,collections,time
D=json.loads(Path('workspace/agent4_higherorthogonal320_pipeline.json').read_text());core=D[0]['found'][0]['support'];co=5;n=11;N=80;full=(1<<N)-1;S=core;target=12;C=[full]+[sum(((x>>j)&1)<<i for i,x in enumerate(S)) for j in range(n)];r=4
start=time.time();hist=collections.Counter();seen=set();profiles={};accepted=0;kd_hist=collections.Counter();new=[]
for proposals in range(10000000):
 for _ in range(4):
  a,b=rng.sample(range(1,target),2);C[a]^=C[b]
 drop=rng.choice([2,3,3,4,4,5]);keep=[full]+rng.sample(C[1:],target-1-drop);cand=extend2(keep,target,N,r)
 if cand is None:hist['dead']+=1
 else:
  kk=key(cand)
  if kk in seen:C=cand;hist['seen']+=1
  else:
   seen.add(kk);kf=N-len(echelon(products(cand,4)))
   if kf!=1:hist['decomp']+=1
   else:
    C=cand;accepted+=1;pts=points(C,N);pd=len(periods(pts)).bit_length()-1;hist['pd'+str(pd)]+=1
    if pd==0:
     kl=N-len(echelon(products(C,3)));kd_hist[kl]+=1
     words=[0]
     for v in C:words +=[w^v for w in words]
     en=tuple(sorted(collections.Counter(w.bit_count() for w in words).items()));profile=(kl,en)
     if profile not in profiles:
      profiles[profile]=len(new);new.append({'support':sorted(pts),'K3':kl,'K4':1,'weightenum':en,'C':C});print('NEWPROFILE',len(new),'K3',kl,'WE',en,'time',time.time()-start,flush=True)
 if time.time()-start>120:break
R={'proposals':proposals+1,'accepted':accepted,'distinct_coordinatecodes':len(seen),'hist':dict(hist),'K3_hist':dict(kd_hist),'profiles':new,'seconds':time.time()-start};Path('workspace/agent4_T80_diverse_profiles.json').write_text(json.dumps(R));Path('workspace/agent4_T80_diverse_profiles.py').write_text(Path('scratchpad.py').read_text().split('#SAVE')[0]);print('FINISHED', {k:v for k,v in R.items() if k!='profiles'},'profiles',len(new))
#SAVE
