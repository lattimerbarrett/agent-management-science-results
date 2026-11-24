import random
from agent2_decomp import witness
from agent2_completion import masks, complete_facets

def check_upper():
    random.seed(33)
    cases=stages=0
    for n,r in [(4,3),(5,3),(6,3),(5,4),(6,4),(6,5)]:
        vertices=[1<<v for v in range(n)]
        allfs=masks(vertices,r)
        for k in (1,2):
            for trial in range(5):
                random.shuffle(allfs)
                fs=frozenset([allfs[0]])
                for f in allfs[1:]:
                    if random.random()<.35 and witness(fs|{f},k) is not None:
                        fs=fs|{f}
                vs=[v for v in vertices if any(v&f for f in fs)]
                buffers=[1<<(n+i) for i in range(r-3)]
                order=complete_facets(fs,k,vs,buffers)
                assert len(order)==len(set(order))
                for f in order:
                    assert f not in fs
                    fs=fs|{f}
                    assert witness(fs,k) is not None,(n,r,k,trial,f)
                    stages+=1
                assert fs==frozenset(masks(vs+buffers,r))
                cases+=1
    return cases, stages

if __name__=='__main__':
    print('Independently checked (input cases, intermediate stages):',check_upper())
