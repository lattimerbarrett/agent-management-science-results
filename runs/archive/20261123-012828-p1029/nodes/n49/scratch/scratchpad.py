import os
print(os.getcwd())
print(os.listdir('.'))
print(os.path.exists('experiments/e1/agent4_reduction_notes.md'))
if os.path.exists('experiments/e1/agent4_reduction_notes.md'):
 print(open('experiments/e1/agent4_reduction_notes.md').read())