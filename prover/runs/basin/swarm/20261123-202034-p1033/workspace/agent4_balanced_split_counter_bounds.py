import math,json
# Rigorous probability-bound checks for the counterexample to balanced-ground splitting.
# Analytic monotonicity handles every r>=1000: exp(.04r)/r^2 increases,
# and log(r/40)<=r/100 follows from value at1000 and derivative1/r<=.01.
checks={}
r=1000;n=r*r;t=n//20
checks['avoid_log_lower_safe']=math.log1p(-1/(20*(1-1/r))) >= -.06
checks['first_union_log_bound_negative']=n*math.log(2)+math.log(t)-math.exp(.04*r)<-1
checks['log_r_over_40_le_r_over_100']=math.log(r/40)<=r/100
checks['second_union_log_upper_coefficient']=math.log(2)+4*(.001+.01+.1-math.log(2))
checks['second_coefficient_negative']=checks['second_union_log_upper_coefficient']<0
assert all(v for k,v in checks.items() if isinstance(v,bool))
assert checks['second_union_log_upper_coefficient'] < -1
print(checks)
with open('workspace/agent4_balanced_split_counter_bounds.json','w') as f:json.dump(checks,f,indent=2)
with open('workspace/agent4_balanced_split_counter_bounds.py','w') as f:f.write(open(__file__).read())
