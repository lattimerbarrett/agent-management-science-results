from pathlib import Path
s=Path('workspace/agent1_negative_spin25.py').read_text()
s=s.replace(" print('S',n,len(S[-1]),flush=True)",' pass')
s=s.replace("json.dump({'prime':p,'columns':cols,'rows':rows,'rank':len(pivs)},open('workspace/agent1_negative_spin25.json','w'))",'')
for a,b in [(-1,1),(-2,3),(-3,2),(-2,1)]:
 nn=-48*a//b-1;r0=24-48*a//b;minn=(r0-12)//2+1
 v=s.replace('p=1000000007;NN=23;D=12;M=NN+D;q=-pow(2,-1,p)%p',f'p=1000000007;NN={nn};D=12;M=NN+D;q=({a})*pow({b},-1,p)%p')
 v=v.replace('sp.Rational(-1,2)',f'sp.Rational({a},{b})').replace('range(19,NN+1)',f'range({minn},NN+1)')
 print('TEST q',a,b,'maxn',nn,flush=True)
 exec(compile(v,'negative_spin','exec'),{'__file__':'noexport'})
if Path(__file__).name=='scratchpad.py':Path('workspace/agent1_negative_spin25_multitest.py').write_text(Path(__file__).read_text())
