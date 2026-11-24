import sys
sys.path.insert(0, 'workspace')
import agent2_order_checks, agent2_tree_checks, agent3_upper_checks, agent3_tree_checks, agent4_tree_checks, agent4_structural_checks
for mod in (agent2_order_checks, agent2_tree_checks, agent3_upper_checks, agent3_tree_checks, agent4_tree_checks, agent4_structural_checks):
    print(mod.__name__, mod.run_checks())
