import json,collections,pathlib
x=json.load(open('workspace/agent3_E256_threeflat382_spectra.json'));S=x['spectra'];raw=json.load(open('workspace/agent3_T280_P12_allorbits.json'))['base_orbits']
res=[]
for i,obj in enumerate(raw):
 found=[]
 for h in range(1,128):
  ip=[]
  for ep in range(2):
   dd=[]
   for d in range(8):
    ar=[]
    for r in range(max(0,d-3),min(d,6)+1):
     ar.extend((c*(1<<(d-r)),r,d-r) for c in range(33) if S[i][h][ep][r]>>c&1)
    dd.append(ar)
   ip.append(dd)
  for ep in range(2):
   highs=[a for a in ip[ep][7] if a[0]>64]
   for q,r,fib in highs:
    assert fib==3 and q in (80,96)
    for d in range(8):
     for q2,r2,fib2 in ip[1-ep][d]:
      for c in range(5):
       for de in range(min(c,1)+1):
        I=q+q2+c-2*de;w=638-2*I
        if w in (310,322,326,330,334):found.append((h,ep,q,d,q2,c,de,w,r2,fib2))
 print(obj['type'],'count',len(found),'weights',collections.Counter(a[7] for a in found), 'sample',found[:3])
 assert all(a[7]==310 for a in found)
 res.append({'type':obj['type'],'candidates':found})
pathlib.Path('workspace/agent3_E256_threeflat382_discretechecks.json').write_text(json.dumps(res,indent=2))
pathlib.Path('workspace/agent3_E256_threeflat382_discretechecks.py').write_text(pathlib.Path('scratchpad.py').read_text())
