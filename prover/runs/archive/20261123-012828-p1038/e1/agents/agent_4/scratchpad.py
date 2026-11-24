from pathlib import Path
p=Path('workspace/agent4_fullmode_pick_check.py');s=p.read_text();s=s.replace('def g(t,z):return t/(z+mp.sqrt(z*z+t*t))', '''def g(t,z):
            root=mp.sqrt(z*z+t*t)
            # RHP nontangential boundary branch at negative imaginary arguments.
            if mp.re(z)==0 and mp.im(z)<-t:root=-root
            return t/(z+root)''');p.write_text(s)
import sys;sys.path.insert(0,'workspace')
import agent4_fullmode_pick_check as a;print(a.check(trials=500))