from itertools import combinations
from functools import lru_cache


def subfaces(f):
    s = f
    while True:
        yield s
        if not s:
            break
        s = (s - 1) & f


def maximal(fs):
    fs = set(fs)
    return tuple(sorted(f for f in fs
                        if not any(f != g and f & g == f for g in fs)))


@lru_cache(None)
def kd(facets, k):
    if len(facets) == 1:
        return True
    sizes = {f.bit_count() for f in facets}
    if len(sizes) != 1:
        return False
    size = next(iter(sizes))
    faces = set().union(*(set(subfaces(f)) for f in facets))
    for s in sorted(faces, key=lambda x: (x.bit_count(), x)):
        if not s or s.bit_count() > k + 1:
            continue
        deletion = maximal(g for g in faces if g & s != s)
        if not deletion or any(g.bit_count() != size for g in deletion):
            continue
        link = maximal(f ^ s for f in facets if f & s == s)
        if kd(deletion, k) and kd(link, k):
            return True
    return False


def exhaustive(n, d, k):
    facets = [sum(1 << v for v in c)
              for c in combinations(range(n), d + 1)]
    full = (1 << len(facets)) - 1
    good = bytearray(full + 1)
    reach = bytearray(full + 1)
    count = 0
    for mask in range(full, 0, -1):
        fs = tuple(sorted(f for i, f in enumerate(facets) if mask >> i & 1))
        good[mask] = kd(fs, k)
        if good[mask]:
            reach[mask] = mask == full or any(
                reach[mask | (1 << i)]
                for i in range(len(facets)) if not (mask >> i & 1))
            union = 0
            for f in fs:
                union |= f
            if union == (1 << n) - 1:
                count += 1
                assert reach[mask], (n, d, k, fs)
    print(dict(n=n, d=d, k=k, tested_k_decomposable=count,
               all_complete_without_new_vertices=True), flush=True)


def search_trap(n, d, timeout_ms=60000):
    import z3
    import json
    fs = [sum(1 << v for v in c)
          for c in combinations(range(n), d + 1)]
    M = len(fs)
    solver = z3.SolverFor('QF_FD')
    solver.set(timeout=timeout_ms)
    rank = {f: z3.Int('r_%d' % f) for f in fs}
    for r in rank.values():
        solver.add(r >= 0, r <= M)
    # Give every included facet a distinct rank; excluded facets get private
    # dummy values outside the included rank range.
    solver.add(z3.Distinct([z3.If(rank[f] < M, rank[f], M+i)
                           for i, f in enumerate(fs)]))
    small = sorted(set().union(*(set(subfaces(f)) for f in fs)) - set(fs))
    mu = {h: z3.Int('m_%d' % h) for h in small}
    number = z3.Sum([z3.If(rank[f] < M, 1, 0) for f in fs])
    for f in fs:
        solver.add(z3.Implies(rank[f] < M, rank[f] < number))
    for v in range(d+1, n-1):
        solver.add(mu[1 << v] < mu[1 << (v+1)])
    for h in small:
        solver.add(mu[h] >= 0, mu[h] <= M)
        rs = [rank[f] for f in fs if f & h == h]
        solver.add(z3.Or([mu[h] == r for r in rs]))
        solver.add([mu[h] <= r for r in rs])
    # By vertex symmetry the first facet is {0,...,d}.
    solver.add(rank[(1 << (d+1))-1] == 0)
    solver.add(z3.Or([r == M for r in rank.values()]))
    for v in range(n):
        solver.add(mu[1 << v] < M)
    for f in fs:
        ridges = [f ^ (1 << v) for v in range(n) if f >> v & 1]
        hs = [h for h in subfaces(f) if h.bit_count() < d]
        for h in hs:
            covering = [mu[r] for r in ridges if r & h == h]
            solver.add(z3.Implies(z3.And(rank[f] < M, mu[h] < rank[f]),
                                  z3.Or([r < rank[f] for r in covering])))
        bad = [z3.And(mu[h] < M,
                      *[mu[r] == M for r in ridges if r & h == h])
               for h in hs]
        solver.add(z3.Implies(rank[f] == M, z3.Or(bad)))
    print('SAT search', n, d, M, flush=True)
    status = solver.check()
    print(status, solver.reason_unknown(), flush=True)
    if status == z3.sat:
        model = solver.model()
        order = sorted([f for f in fs if model.eval(rank[f]).as_long() < M],
                       key=lambda f: (model.eval(rank[f]).as_long(), f))
        faces = {0}
        for f in order:
            old_ridges = [r for r in subfaces(f) if r.bit_count() == d and r in faces]
            if len(faces) > 1:
                assert all(any(h & r == h for r in old_ridges)
                           for h in subfaces(f) if h in faces)
            faces.update(subfaces(f))
        for f in set(fs)-set(order):
            old_ridges = [r for r in subfaces(f) if r.bit_count() == d and r in faces]
            assert any(not any(h & r == h for r in old_ridges)
                       for h in subfaces(f) if h in faces)
        print('VERIFIED', order, flush=True)
        with open('trap.json', 'w') as out:
            json.dump(dict(n=n, d=d, order=order), out)
    return status

def greedy_search(n, runs=100, samples=12):
    import numpy as np
    import random, time, json
    verts = np.array([[1 << v for v in c] for c in combinations(range(n), 4)], dtype=np.int64)
    fs = verts.sum(axis=1)
    ridges = fs[:, None] ^ verts
    subsets = [[s for s in subfaces(int(f))] for f in fs]
    alltri = np.array([sum(1 << v for v in c) for c in combinations(range(n), 3)])
    def choices(p):
        rr = p[ridges]
        sigmas = (rr * verts).sum(axis=1)
        count = rr.sum(axis=1)
        return np.flatnonzero((count > 0) & (count < 4) & ~p[sigmas])
    start = time.time()
    for run in range(runs):
        p = np.zeros(1 << n, dtype=np.bool_)
        order = [int(fs[0])]
        p[subsets[0]] = True
        # Introduce each vertex by attaching a tetrahedron on an existing ridge.
        for v in range(4, n):
            oldridges = [s for s in alltri if s < (1 << v) and p[s]]
            r = int(random.choice(oldridges))
            f = r | (1 << v)
            order.append(f)
            p[list(subfaces(f))] = True
        while True:
            cs = choices(p)
            if not len(cs):
                if not p[alltri].all():
                    for i, f in enumerate(fs):
                        if p[ridges[i]].all() and int(f) not in order:
                            order.append(int(f))
                            p[subsets[i]] = True
                    # Verify every step directly, without the vectorized rule.
                    old = {0}
                    for step, f in enumerate(order):
                        rr = [r for r in subfaces(f) if r.bit_count() == 3 and r in old]
                        if step:
                            assert all(any(h & r == h for r in rr)
                                       for h in subfaces(f) if h in old)
                        old.update(subfaces(f))
                    for f in fs:
                        f = int(f)
                        if f not in old:
                            rr = [r for r in subfaces(f) if r.bit_count() == 3 and r in old]
                            assert any(not any(h & r == h for r in rr)
                                       for h in subfaces(f) if h in old)
                    result = dict(n=n, d=3, order=order)
                    print('VERIFIED TRAP', result, flush=True)
                    with open('trap.json', 'w') as out:
                        json.dump(result, out)
                    return result
                break
            if samples > 1:
                options = random.sample(list(cs), min(samples, len(cs)))
                scores = []
                for i in options:
                    changed = [s for s in subsets[i] if not p[s]]
                    p[changed] = True
                    scores.append(len(choices(p)) + random.random())
                    p[changed] = False
                i = options[min(range(len(options)), key=lambda j: scores[j])]
            else:
                # Prefer edge-restriction moves, which add two triangles at once.
                rr = p[ridges[cs]]
                counts = rr.sum(axis=1)
                opts = cs[counts == counts.min()]
                i = int(random.choice(opts))
            order.append(int(fs[i]))
            p[subsets[i]] = True
        if run % 20 == 0:
            print('greedy', n, run, round(time.time()-start, 2), flush=True)
    return None

if __name__ == '__main__':
    for n in [10, 12, 15, 18]:
        if greedy_search(n, runs=100, samples=8):
            break
