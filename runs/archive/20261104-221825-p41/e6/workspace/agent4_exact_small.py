from itertools import combinations
from functools import lru_cache
import json,os,time

def maximal(fs):
 fs=set(fs)
 return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))
@lru_cache(None)
def kd(fs,k):
 if len(fs)==1:return True
 if not fs:return False
 n=max(fs).bit_length()
 for size in range(1,min(k+1,fs[0].bit_count())+1):
  for vs in combinations(range(n),size):
   b=sum(1<<v for v in vs)
   containing=[f for f in fs if f&b==b]
   if not containing:continue
   link=maximal(f^b for f in containing)
   de=tuple(f for f in fs if f&b!=b)
   if not de:continue
   if any(not any((f^(1<<v))&g==(f^(1<<v)) for g in de) for f in containing for v in vs):continue
   if kd(de,k) and kd(link,k):return True
 return False

def attach(fs,f):
 ints=maximal(f&g for g in fs)
 return all(x.bit_count()==f.bit_count()-1 for x in ints)

@lru_cache(None)
def shellable(fs):
 if len(fs)==1:return True
 for i,f in enumerate(fs):
  de=fs[:i]+fs[i+1:]
  if attach(de,f) and shellable(de):return True
 return False

def check(n=6,d=3):
 t=time.time()
 ff=[sum(1<<i for i in x) for x in combinations(range(n),d+1)]
 N=len(ff);ALL=(1<<N)-1
 good={k:bytearray(1<<N) for k in [1,3]}
 counts={1:0,3:0}
 for state in range(1,ALL+1):
  fs=tuple(ff[j] for j in range(N) if state>>j&1)
  sh=shellable(fs)
  for k in [1,3]:
   good[k][state]=kd(fs,k)
   counts[k]+=good[k][state]
  assert sh==bool(good[3][state]),(state,fs)
 completable={k:bytearray(1<<N) for k in [1,3]}
 for k in [1,3]:
  completable[k][ALL]=1
  for state in range(ALL-1,0,-1):
   if not good[k][state]:continue
   completable[k][state]=any(completable[k][state|(1<<j)] for j in range(N) if not state>>j&1)
  assert all(not good[k][s] or completable[k][s] for s in range(1,ALL+1))
 result={'n':n,'d':d,'states':ALL,'k_decomposable_counts':counts,'all_k1_and_k3_states_completable':True,'k3_iff_shellable':True,'seconds':time.time()-t}
 print(result,flush=True)
 return result

if __name__=='__main__':
 result=check()
 os.makedirs('workspace',exist_ok=True)
 with open('workspace/agent4_exact_small.json','w') as f:json.dump(result,f,indent=2)
 with open('scratchpad.py') as f:src=f.read()
 with open('workspace/agent4_exact_small.py','w') as f:f.write(src)
