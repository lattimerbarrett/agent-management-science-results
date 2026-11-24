import json,hashlib,itertools
raw=open("workspace/a3_rejected_n16_candidate.json").read()
c=json.load(open("workspace/a3_rejected_n16_homology_certificate.json"))
assert hashlib.sha256(raw.encode()).hexdigest()==c["sha256"]
fs=json.loads(raw);z={int(k):v for k,v in c["cycle"].items()};u={int(k):v for k,v in c["cochain"].items()};p=c["field"]
E={sum(1<<i for i in cc) for f in fs for cc in itertools.combinations([i for i in range(f.bit_length()) if f>>i&1],2)}
T={sum(1<<i for i in cc) for f in fs for cc in itertools.combinations([i for i in range(f.bit_length()) if f>>i&1],3)}
assert set(z)<=E and set(u)<=E
bz={}
for e,a in z.items():
 vv=[i for i in range(e.bit_length()) if e>>i&1]
 for j,v in enumerate(vv):bz[e^(1<<v)]=(bz.get(e^(1<<v),0)+(-1)**j*a)%p
assert not any(bz.values())
for t in T:
 vv=[i for i in range(t.bit_length()) if t>>i&1]
 assert sum((-1)**j*u.get(t^(1<<v),0) for j,v in enumerate(vv))%p==0
assert sum(a*u.get(e,0) for e,a in z.items())%p!=0
print("Verified explicit nonzero H1(GF3) certificate: this terminal complex cannot be shellable.")
