"""Fixed-top-form gap lemma (agent_3 proof, independently checked by agent_2).

For F in RM(6,12) whose homogeneous degree6 part, after a linear change,
is z*(a1*a2*a3*a4*a5+b1*b2*b3*b4*b5) and hence avoids a twelfth variable t,
its weight cannot be136 or144.

Let v=Delta_t F on the other11 variables. Since all degree6 monomials
avoid t, deg(v)<=4. Also wt(v)<=wt(F)<=144. A nonzero RM(4,11) word
therefore has wt(v)=128 by its first two distinct weights128,192.
Its support D is an affine7-flat. Write F=u+t*v, deg(u)<=6. Then
wt(F)=128+2*wt(u outside D). For target weights136,144, the latter
outside weight is4,8. But any nonzero degree<=6 function outside a
proper flat D in11 variables has outside weight>=16: choose an affine
hyperplane containing D and excluding some outside support point;
the restriction on its complement is a nonzero RM(6,10) word.
Thus v=0, and F is independent of t.

Delete t to obtain F' in RM(6,11), weight68 or72. Its degree6 part is
z times the cross-star5 form. Its z-slices P,Q both lie RM(5,10),
and their homogeneous degree5 parts sum to vol(A5)+vol(B5).
If both are nonzero, the smaller has weight<=36, and so weight32
(first two distinct RM(5,10) weights32,48). The partner would have
weight36 or40, impossible. If one is zero, the other has cross-star
homogeneous part. Weight/2 modulo2 depends only on the degree5 part
in RM(5,10), and equals1 for this part: complementary monomials
have supports intersecting in exactly one point. Therefore the other
slice's weight is2 mod4, contradicting68 or72. QED.

Only standard RM minimum, second-weight, and minimum-word affine-flat
facts enter. The numerical checks below are supplemental, not an
exhaustive enumeration of all polynomials.
"""

def verify_numerical_bounds():
    for w in (136,144):
        assert 128<=w<192
        e=(w-128)//2
        assert 0<e<2**(11-1-6)
        smaller_max=(w//2)//2
        assert 32<=smaller_max<48
        partner=w//2-32
        assert 32<partner<48
        assert (w//2)%4==0
    # Directly verify the q=1 cross-star on ten variables.
    cross=0
    for x in range(1024):
        v=(int((x&31)==31)^int((x>>5)==31))
        cross += v
    assert cross==62 and (cross//2)%2==1
    print('Fixed-top L124 gap numerical checks passed for weights136,144.')

if __name__=='__main__': verify_numerical_bounds()
