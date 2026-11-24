"""Exact image-module bases over Z/p^e, retaining nonunit pivots.
Used for checked mod9 rank3 Johnson-image calculations.
"""
from pathlib import Path
import pickle,itertools,random,time
from agent3_derivations import add,bracket,generators

def module_basis(vectors,p=3,exponent=2):
    modulus=p**exponent;piv={}
    def valuation(v):
        r=0
        while v%p==0:r+=1;v//=p
        return r
    for a0 in vectors:
        queue=[a0]
        while queue:
            a=queue.pop().copy()
            while a:
                key=min(a);v=valuation(a[key])
                if key in piv:
                    b=piv[key];w=valuation(b[key])
                    if v>=w:
                        a=add(a,b,-(a[key]//(p**w)),modulus);continue
                    queue.append(piv.pop(key))
                inv=pow(a[key]//(p**v),-1,modulus)
                a={k:t*inv%modulus for k,t in a.items() if t*inv%modulus}
                piv[key]=a
                if v:
                    extra={k:t*p**(exponent-v)%modulus for k,t in a.items() if t*p**(exponent-v)%modulus}
                    if extra:queue.append(extra)
                break
    return list(piv.values())

def membership(a,bs,p=3,exponent=2):
    modulus=p**exponent
    a={k:int(v)%modulus for k,v in a.items() if int(v)%modulus}
    piv={min(b):b for b in bs}
    while a:
        k=min(a)
        if k not in piv:return False
        b=piv[k]
        if a[k]%b[k]:return False
        a=add(a,b,-a[k]//b[k],modulus)
    return True

def selftest():
    rng=random.Random(1729)
    def span(vs):
        return {tuple(sum(c*v.get((i,),0) for c,v in zip(cs,vs))%9 for i in range(3))
                for cs in itertools.product(range(9),repeat=len(vs))}
    for trial in range(20):
        vs=[{(i,):rng.randrange(9) for i in range(3)} for j in range(3)]
        vs=[{k:v for k,v in a.items() if v} for a in vs]
        assert span(vs)==span(module_basis(vs))
    print('finite exhaustive module-span selftests passed')

if __name__=='__main__':
    selftest()
    bs=generators(3,9);gs=bs
    for c in range(2,9):
        cache=Path(f'workspace/agent3_IA3_mod9_degree{c}_basis.pkl')
        if cache.exists():bs=pickle.loads(cache.read_bytes())
        else:
            bs=module_basis(bracket(a,b,3,9) for a in gs for b in bs)
            cache.write_bytes(pickle.dumps(bs))
        print(c,len(bs),flush=True)
    tau=pickle.load(open('workspace/agent4_candidate_tau8.pkl','rb'))
    assert membership(tau,bs)
    print('candidate tau8 belongs to full mod9 Johnson-image module')
