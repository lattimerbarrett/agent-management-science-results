from pathlib import Path
parts=[]
for name in ['agent2_lambda7.py','agent3_D7.py','agent3_d9.py']:
 t=Path('workspace/'+name).read_text().split("if __name__=='__main__':")[0]
 if name=='agent3_d9.py':t=t.replace('def certificate():','def d9_certificate():')
 parts.append(t)
parts.append(Path('workspace/agent1_binomial.py').read_text().split("if __name__=='__main__':")[0])
parts.append('''
def run_all():
    lam7=intersecting_upsets(6)[0]
    D7=compute_D7()[0]
    assert lam7==1422564 and D7==2414682040998
    print('lambda7=',lam7,'D7=',D7)
    check()
    D=D7
    for d in range(10,14):
        D=D*(D+1)//2
        assert D<2**exponent(d)
    counts,sums=d9_certificate()
    assert sum(sums)>D7+1
    print('d9 certificate=',sum(sums))
    from agent3_lower_checks import check_standard_example
    assert check_standard_example()[0]==48
    exec(compile(open('workspace/agent4_root_doubling.py').read(),'root.py','exec'),{})
    assert 2*783558>lam7+1
    exec(compile(open('workspace/agent4_hansel.py').read(),'hansel.py','exec'),{})
    exec(compile(open('workspace/agent4_embedding.py').read(),'embedding.py','exec'),{})
    print('ALL CHECKS PASSED')
if __name__=='__main__':run_all()
''')
text='\n'.join(parts)
Path('workspace/final_check.py').write_text(text)
import sys
sys.path.insert(0,'workspace')
exec(compile(text,'workspace/final_check.py','exec'))
