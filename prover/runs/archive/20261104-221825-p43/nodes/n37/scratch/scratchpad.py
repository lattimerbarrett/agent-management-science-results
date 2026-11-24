import math
area=4*math.pi
print('Recapping by k times either sphere shifts action by -4*pi*k and grading by -4*k.')
print('Three strictly ordered capped carriers need not be three geometric fixed points:')
carriers=[('p, trivial capping',2*area),('q, trivial capping',1.5*area),('p, sphere-recapped',area)]
for name,action in carriers: print(name, 'action/(4*pi) =',action/area)
print('Distinct underlying points:',len({name.split(',')[0] for name,_ in carriers}))
print('Sufficient extra input: all three actions belong to one interval of length strictly less than 4*pi.')
