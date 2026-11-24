"""Independent formula for h1(O) via fibre-filtration Hankel differentials."""
import sympy as sp

def h1_O(g,b):
    r=(g+2)//3
    assert g>=2 and len(b)==r
    loss=0
    for n in range(1,g+r-1):
        rows=(g+r-2-n)//2+1
        cols=n//2+1
        H=sp.Matrix(rows,cols,lambda i,j:b[i+j] if i+j<r else 0)
        loss+=H.rank()
    return g*g-loss

def closed_O_L(g,b):
    r=(g+2)//3
    s=max((j+1 for j,c in enumerate(b) if c),default=0)
    loss=s*(g+r+1-2*s)
    if s==0:
        return g*g,5*g*g-7*g+3
    return g*g+1-loss,5*g*g-7*g+3-loss

if __name__=='__main__':
    for g in range(2,13):
        r=(g+2)//3
        print(g, [h1_O(g,[int(j==a) for j in range(r)]) for a in range(r)])
