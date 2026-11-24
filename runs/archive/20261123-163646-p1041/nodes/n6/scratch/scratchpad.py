def family(m):
    n=2**m
    return {0,n}|set(range(6000,10001,2))|set(range(n-10000,n-6000+1,2))
for m in (14,15,16):
    s=family(m)
    n=2**m
    print(m, 'symmetric:', all(n-w in s for w in s), '10300 present:',10300 in s, '8100 present:',8100 in s, 'low count:',sum(w<=8192 for w in s))
# A simpler example, a fixed list of singleton intervals (not fixed order).
for m in (14,15):
    n=2**m
    s={0,10000,n-10000,n}
    print('singleton family',m,sorted(s), '6384 present:',6384 in s)
