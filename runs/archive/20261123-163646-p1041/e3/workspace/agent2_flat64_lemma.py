"""A proved special case of exclusion; NOT a complete exclusion proof.

Lemma. Let A be the indicator of a linear 6-flat in F2^14, and let B be
any set with A+B in augmentation ideal I^7 and AB=J (group algebra).
Then |B| is not in {258,262,266,270}.

Proof. Split coordinates x in F2^8, y in F2^6 so A={0}xF2^6.
The convolution equation says each B_x is odd. Write |B|=256+2e,
e<=7, and let D be rows of size>1; |D|<=e. Its y-moments
b_T(x)=sum_{y in B_x} product_{i in T} y_i, for 1<=|T|<=4,
have degree<=|T|+1, since all their x-moments through degree
6-|T| vanish (A's corresponding moment is zero).
Put phi_i=b_{i}, degree<=2. Outside D, b_T=product phi_i.
For |T|=2 the difference has degree<=4, so if nonzero its weight
is>=16; |D|<=7 forces zero. After translation of each row by phi(x),
all moments of degrees1,2 vanish. An odd row differing from {0}
then has size>=7: its symmetric difference with {0} is a nonzero
null2 set and has size>=8. Thus |D|<=floor(2e/6)<=2.
For |T|=3, product phi_i has degree<=5, using one pair (degree<=3)
and one singleton (degree<=2). The discrepancy has degree<=5,
minimum nonzero weight8, and support<=2, so is zero. Hence each
nontrivial translated odd row has size>=15 and |D|<=floor(2e/14)<=1.
For |T|=4, pair the factors: degree<=6. Discrepancy degree<=6,
minimum weight4, support<=1, hence zero. Each exceptional row now
has size>=31, contradicting its excess<=2e<=14. Thus D is empty,
which would force |B|=256. QED.

The null-k minimum 2^(k+1) used above is the usual RM minimum-weight
bound, or follows by induction using any hyperplane splitting a
nonempty null-k set into two nonempty null-(k-1) sets.
"""

def verify_numerical_bounds():
    n=8
    for e in (1,3,5,7):
        D=e
        assert D < 2**(n-4)
        D=(2*e)//6
        assert D < 2**(n-5)
        D=(2*e)//14
        assert D < 2**(n-6)
        assert 2*e < 30
    print('Numerical bounds for flat64 exclusion lemma verified.')
if __name__=='__main__': verify_numerical_bounds()
