from fractions import Fraction
import json
# Exact checks of the finite nonadditivity witness. For eta=p/q,
# N=floor(q/p)+1 guarantees N*eta>1. A bounded positive partial
# sum has quasitrace <=1 by positivity and linearity with its complement.
checks=0
for p in range(1,201):
    for q in range(1,201):
        eta=Fraction(p,q)
        N=q//p+1
        assert N*eta>1
        # Telescoping coefficients of sum (a[k+1]-a[k])
        # are exactly coefficients of a[N]-a[0].
        coeff=[0]*(N+1)
        for k in range(N):
            coeff[k]-=1
            coeff[k+1]+=1
        assert coeff==[-1]+[0]*(N-1)+[1]
        checks+=1
report={'verified_rational_eta_cases':checks,
        'scope':'Finite-sum nonadditivity witness only; not existence or the claimed 1/3 bound',
        'endpoint_eta':'1/3','endpoint_N':4,
        'endpoint_sum_of_increment_quasitraces':'4/3',
        'partial_sum_quasitrace_upper_bound':1}
with open('workspace/agent3_nonadditivity_checks.json','w') as f:
    json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))