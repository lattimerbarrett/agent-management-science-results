from pathlib import Path
root=Path('experiments/e1')
for p in sorted(root.glob('*.md')):
    text=p.read_text()
    if any(w in text.lower() for w in ['bessel','projection family','projection families']):
        print('\nFILE:',p)
        for key in ['Bessel','bessel','projection family','projection families']:
            pos=text.find(key)
            if pos>=0:
                print(text[max(0,pos-350):pos+1600]);break
