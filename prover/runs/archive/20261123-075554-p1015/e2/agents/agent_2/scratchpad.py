import pathlib,itertools,json
source='''import itertools,json\nchecks=0\nfor n in range(1,5):\n    U=set(range(n))\n    for f in itertools.product(range(n),repeat=n):\n        for mask in range(1<<n):\n            KB={i for i in U if mask>>i&1}\n            KA={i for i in U if f[i] in KB}\n            assert U-KA=={i for i in U if f[i] in U-KB}\n            checks+=1\nprint(json.dumps({'checks':checks}))\n'''
pathlib.Path('workspace/agent2_pullback_checks.py').write_text(source)
exec(compile(source,'workspace/agent2_pullback_checks.py','exec'))
