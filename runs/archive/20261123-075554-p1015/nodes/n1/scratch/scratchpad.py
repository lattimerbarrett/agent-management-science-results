from itertools import product
# P: the set is Pi^0_2; W: its degree is weakly cototal;
# C: its skip has cototal degree.
models = [(P,W,C) for P,W,C in product([False,True], repeat=3)
          if (not P or W) and (not W or C)]
print('Models with a Pi^0_2 set and a noncototal skip:',
      [v for v in models if v[0] and not v[2]])
print('Models with weak cototality and a noncototal skip:',
      [v for v in models if v[1] and not v[2]])