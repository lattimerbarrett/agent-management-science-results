"""Exact elementary consequences of a strict sub-n/r Turan surplus bound.
No third-party packages needed. The assertions verify arithmetic identities used
in agent_2's template-reduction lemma, not the unavailable global structure.
"""
def turan(n,r):
    q,s=divmod(n,r)
    return (n*n - s*(q+1)**2 - (r-s)*q*q)//2

def apex_excess(n,r):
    return n-1+turan(n-1,r)-turan(n,r)

def cycle_template_excess(n,r,h):
    # Put vertex-disjoint (h+1)-cycles in a largest Turan class.
    m=(n+r-1)//r
    return m//(h+1)*(h+1)

def component_bound(h):
    # Internal degree < h, no path on 2h vertices.
    # BFS depth <=2h-2; simple safe overcount.
    return sum((h-1)**j for j in range(2*h-1))

def check(limit=300):
    for r in range(2,12):
        for n in range(2,limit):
            assert apex_excess(n,r)==(n+r-1)//r-1
            for h in range(3,12):
                x=cycle_template_excess(n,r,h)
                assert x>=(n+r-1)//r-h
    return True

if __name__=='__main__':
    print('Exact arithmetic checks:',check())
    for h in range(3,8):
        print('h=',h,'safe internal component bound=',component_bound(h))


def strict_template_lemma_summary():
    return {
        'proved': [
          'apex surplus ceil(n/r)-1',
          'cycle-factor surplus at least ceil(n/r)-h',
          'a<1/r forces star and path internal embeddings',
          'complete-cross templates then have bounded internal components',
          'their H-embedding status depends only on component multiplicities truncated at h',
          'in any unbounded feasible box, repeatable components are trees and occur nontrivially in at most one part',
        ],
        'not_proved': [
          'global cycle-extremizer reduction to complete-cross templates',
          'exact matching-only recoloring lemma below threshold',
          'boundary r>=3 rigidity',
        ],
    }
