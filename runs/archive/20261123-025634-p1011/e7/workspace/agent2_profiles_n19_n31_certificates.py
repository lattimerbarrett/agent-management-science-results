from pathlib import Path
import math,re
source=Path('workspace/agent2_polynomial_search.py').read_text()
source='\n'.join(line for line in source.splitlines() if not ('Path(' in line and 'write_text' in line))
roots=[.902430998863571,.8587674198799999,.8449730421326679,.8373851342317891,.8324948173240954,.8291359557962843,.826765066866965,.8250793059139625,.8238911685112127,.8230761131213411,.8225470901006374,.8222408623260689,.8221101098843723]
for N,root in zip(range(19,32),roots):
    L=math.floor(root*10**10)
    modified=source.replace('N=19;','N='+str(N)+';')
    modified=re.sub(r'Z=\(s\.Rational\(9024309988,10\*\*10\),s\.Rational\(9024309989,10\*\*10\)\)',f'Z=(s.Rational({L},10**10),s.Rational({L+1},10**10))',modified)
    assert '9024309988' not in modified or N==19
    # Numerical root finding is only diagnostic; the final assertions are exact intervals.
    print('\nCERTIFY DIMENSION',N,flush=True)
    exec(modified,{})
print('ALL dimensions19 through31 have exact full-minimum interval certificates.')
Path('workspace/agent2_profiles_n19_n31_certificates.py').write_text(Path(__file__).read_text())
