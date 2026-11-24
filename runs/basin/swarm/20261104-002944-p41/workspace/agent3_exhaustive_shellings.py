import itertools,json

def check(n,d):
 fs=[sum(1<<x for x in s) for s in itertools.combinations(range(n),d+1)]; m=len(fs)
 faceindex={g:i for i,g in enumerate(range(1<<n))}
 subbits=[sum(1<<g for g in range(1<<n) if g&f==g) for f in fs]
 rds=[[f^(1<<x) for x in range(n) if f>>x&1] for f in fs]
 closure=[0]*(1<<m)
 reachable=bytearray(1<<m); extendable=bytearray(1<<m)
 reachable[0]=1
 eligible=[0]*(1<<m)
 for mask in range(1,1<<m):
  bit=mask&-mask;j=bit.bit_length()-1;closure[mask]=closure[mask^bit]|subbits[j]
 for mask in range(1<<m):
  faces=closure[mask]
  for j,f in enumerate(fs):
   if mask>>j&1:continue
   intersection=faces&subbits[j]
   cover=0
   for r in rds[j]:
    if faces>>r&1:cover|=sum(1<<g for g in range(1<<n) if g&r==g)
   if mask==0 or (cover and intersection&~cover==0):eligible[mask]|=1<<j
   if reachable[mask] and eligible[mask]>>j&1:reachable[mask|1<<j]=1
 extendable[-1]=1
 for mask in range((1<<m)-2,-1,-1):
  choices=eligible[mask]
  while choices:
   bit=choices&-choices;choices^=bit
   if extendable[mask|bit]:extendable[mask]=1;break
 bad=[mask for mask in range(1<<m) if reachable[mask] and not extendable[mask]]
 print({'n':n,'d':d,'facets':m,'shellable_states':sum(reachable),'bad_states':len(bad)})
 assert not bad
if __name__ == '__main__':
 check(6,3)
