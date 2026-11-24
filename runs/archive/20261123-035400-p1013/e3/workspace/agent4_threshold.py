from fractions import Fraction as F

def cycle_advantage(r,s):
    alpha=F(s-1,s)
    D=F((s-2)*(s-3),2*s)
    return -F(2*r,r-2)+F(4*r,(r-1)*(r-2))*alpha+F(2*r,(r-1)**2)*D

if __name__ == '__main__':
    for r in range(3,31):
        s=next(s for s in range(2,3*r+5) if cycle_advantage(r,s)>0)
        assert s == (6 if r==3 else 9 if r==4 else 2*r+1)
        print(r,s,cycle_advantage(r,s))
    assert cycle_advantage(4,8)==0
