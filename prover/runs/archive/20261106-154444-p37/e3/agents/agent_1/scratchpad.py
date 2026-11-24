import sys,time,json
sys.path.insert(0,'workspace')
from agent2_lambda8_certificate import count_lambda
from agent2_dedekind7_certificate import count_dedekind
from agent4_trees import check as trees
from agent1_finite_grid_certificate import main as grids
from fractions import Fraction
start=time.time()
for k,expected in [(7,1422564),(8,229809982112)]:
 v,s=count_lambda(k); assert v==expected;print('lambda',k,v,'states',s,flush=True)
v,s=count_dedekind(7);assert v==2414682040998;print('D7',v,s,flush=True)
assert 2**90>v**2 and 2**690>v**16
trees();grids()
assert 29**10<2**17*9**10
assert 399*398*126>20*10**6
assert 90*1000<2**20
assert Fraction(17,10)+Fraction(1,1000)+Fraction(85050,10**6)<Fraction(9,5)
assert 600*3**24<4**24
assert Fraction(199,100)*Fraction(99,100)>Fraction(19,10)
assert 128**2<14*35**2
print('MASTER ALL PASS',time.time()-start)
