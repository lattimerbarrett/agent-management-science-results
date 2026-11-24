import itertools,time,json,collections,shutil,pickle
MASK=(1<<128)-1;start=time.time()
def span(B):
 S=[0]
 for b in B:S += [x^b for x in S]
 return S
def flat(B):return sum(1<<x for x in span(B))
def trans(f,i):
 st=1<<i;lo=LOW[i];d=(f^(f>>st))&lo;return f^d^(d<<st)
def cnot(f,dst,src):
 st=1<<dst;lo=CM[dst,src];d=(f^(f>>st))&lo;return f^d^(d<<st)
LOW=[sum(1<<x for x in range(128) if not(x>>i&1)) for i in range(7)];CM={(d,s):sum(1<<x for x in range(128) if x>>s&1 and not(x>>d&1)) for d in range(7) for s in range(7) if d!=s}
def allflats(k):
 out=[]
 for piv in itertools.combinations(range(7),k):
  free=[(i,j) for i,p in enumerate(piv) for j in range(p+1,7) if j not in piv]
  for a in range(1<<len(free)):
   B=[1<<p for p in piv]
   for z,(i,j) in enumerate(free):
    if a>>z&1:B[i]^=1<<j
   f=flat(B);cos=[f]
   for j in range(7):
    if j not in piv:cos += [trans(g,j) for g in cos]
   out.extend(cos)
 return out
D3=allflats(3);D4=allflats(4);print('ENUM',len(D3),len(set(D3)),len(D4),len(set(D4)),'t',time.time()-start,flush=True);assert len(D3)==len(set(D3))==188976 and len(D4)==len(set(D4))==94488
G=flat([1,2,4])^flat([8,16,32]);gens=[(d,s) for block in [range(3),range(3,6)] for d in block for s in block if d!=s]+[(d,6) for d in range(6)]+[None]
def image(f,op):
 if op is not None:return cnot(f,*op)
 for a in range(3):
  b=a+3;f=cnot(cnot(cnot(f,a,b),b,a),a,b)
 return f
assert all(image(G,op)==G for op in gens)
left=set(D3);reps=[];sizes=[]
while left:
 root=left.pop();Q=[root]
 for f in Q:
  for op in gens:
   g=image(f,op)
   if g in left:left.remove(g);Q.append(g)
 reps.append(root);sizes.append(len(Q))
print('ORBITS',len(reps),'sizes',collections.Counter(sizes),'sum',sum(sizes),'t',time.time()-start,flush=True);assert sum(sizes)==188976
C=[(G&k).bit_count() for k in D4];profiles={}
for ri,f in enumerate(reps):
 a=(f&G).bit_count();fg=f&G
 for k,c in zip(D4,C):
  b=(f&k).bit_count();t=(fg&k).bit_count();pr=(8,14,22-2*a,16,24-2*b,30-2*c,38-2*(a+b+c)+4*t)
  if pr not in profiles:profiles[pr]=(f,G,k)
 if ri%10==0:print('profileorbit',ri,'profiles',len(profiles),'t',round(time.time()-start,2),flush=True)
pickle.dump({'profiles':profiles,'orbit_reps':reps,'orbit_sizes':sizes,'flats3_count':len(D3),'flats4_count':len(D4)},open('workspace/agent3_exact_8_14_16_profiles.pkl','wb'));json.dump([{'weights':list(pr),'functions':list(map(hex,F))} for pr,F in sorted(profiles.items())],open('workspace/agent3_exact_8_14_16_profiles.json','w'));print('DONEprofiles',len(profiles),'orbits',len(reps),'t',time.time()-start,flush=True);shutil.copyfile(__file__,'workspace/agent3_exact_8_14_16_profiles.py')
