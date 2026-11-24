import runpy
D=runpy.run_path('agents/agent_1/scratchpad.py')
a_rank=D['a_rank']
checks=0
for s in (1,2,3):
    q=49
    h=s*q//(3*s-1)
    for r in sorted(set((0,1,h,h+1,q))):
        rank=a_rank(s,r,q)
        defect=3*s*(q-1) if r==0 else max(3*s*q-3*(3*s-1)*r,0)
        assert rank==3*(s*q+r)-defect, (s,r,rank,defect)
        checks+=1
print('Additional q=49 multiplication checks passed:',checks)
