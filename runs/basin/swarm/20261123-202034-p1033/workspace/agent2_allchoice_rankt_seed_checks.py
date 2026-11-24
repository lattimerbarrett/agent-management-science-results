from itertools import combinations,product
from pathlib import Path
import json,time

def allchoice_tournament(coresizes):
    t=len(coresizes);out=[[] for _ in range(t)]
    for i,j in combinations(range(t),2):
        n=t if t%2 else t+1
        a,b=(i,j) if (j-i)%n<=n//2 else (j,i)
        out[a].append(b)
    X=[];n=0
    for c in coresizes:X.append(set(range(n,n+c)));n+=c
    H=[];owners=[]
    for i in range(t):
        for P in product(*(sorted(X[j]) for j in out[i])):
            H.append(sum(1<<x for x in X[i]|set(P)));owners.append(i)
    return X,H,owners,n,out

def exactcovers(X,H,n,t):
    covers=[];xm=[sum(1<<x for x in C) for C in X]
    tested=0
    for r in range(t+1):
        for cc in combinations(range(n),r):
            tested+=1;C=sum(1<<x for x in cc)
            if all(C&F for F in H):
                assert r==t,(r,t)
                for K in xm:
                    assert C&K==K or (C&K).bit_count()<=1
                covers.append(C)
    assert covers
    return covers,tested

start=time.time();cs=[5]*5;locked=[];rows=[]
for i in range(5):
    while True:
        X,H,own,n,out=allchoice_tournament(cs)
        assert all(F&G for F,G in combinations(H,2))
        C,tested=exactcovers(X,H,n,5)
        xm=sum(1<<x for x in X[i]);exhaust=[c for c in C if c&xm==xm]
        rows.append(dict(core_sizes=cs[:],selected_class=i,edges=len(H),ground=n,
                         subsets_tested=tested,minimum_covers=len(C),exhausts_selected=bool(exhaust)))
        if exhaust:
            seed=exhaust[0];A=[];L=[]
            for j,K in enumerate(X):
                hit=[x for x in K if seed>>x&1]
                if j!=i and hit:L.append(j)
            variants=[xm|sum(1<<x for x in choices) for choices in product(*(sorted(X[j]) for j in L))]
            assert all(v.bit_count()==5 for v in variants)
            assert all(v&F for v in variants for F in H)
            assert all(v&w for v,w in combinations(variants,2))
            # All variants here are already original edges, as expected for tournaments.
            assert set(variants)<=set(H)
            locked.append(i);break
        cs[i]-=1
assert cs==[3]*5
# Explicit rank-t seed addition check in nontrivial duplicate-center upper family.
m=2;n=8;T=m*n;c=T-n+1;r=n-2*m;ell=m*(2*m-1);D=r+ell
E=list(combinations(range(n),2));edgeid={e:j for j,e in enumerate(E)}
stars=[{edgeid[tuple(sorted((a,b)))] for b in range(n) if a!=b} for a in range(n)]
base=[]
for owner in range(T):
    a=owner//m
    for pp in combinations(sorted(stars[a]),r):
        P=set(pp);omitted=[b for b in range(n) if b!=a and edgeid[tuple(sorted((a,b)))] not in P]
        targets={m*b+s for b in omitted for s in range(m)}
        assert len(targets)==ell
        base.append((owner,P,targets))
seedchecks=0
for i in range(T):
    a=i//m;Ai=stars[a]
    assert c+len(Ai)==T and len(Ai)<=D
    for h,P,target in base:
        assert h==i or Ai&P or i in target
        seedchecks+=1
    for j in range(i):assert Ai&stars[j//m]
summary=dict(tournament=dict(stages=rows,final_core_sizes=cs,classes_locked=locked,
                             total_actual_cover_subsets=sum(z['subsets_tested'] for z in rows)),
             nontrivial_star_seed_addition=dict(t=T,core_size=c,old_member_rank=c+D,new_seed_rank=T,
                   base_patterns=len(base),seed_old_pattern_checks=seedchecks,new_seed_pairs=T*(T-1)//2),
             runtime=time.time()-start)
print(json.dumps(summary,indent=2))
Path('workspace/agent2_allchoice_rankt_seed_checks.json').write_text(json.dumps(summary,indent=2))
