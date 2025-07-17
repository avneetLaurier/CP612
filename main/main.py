import sys
import os
from sort_data import sort_by_variousId
from source_data import load_file #load_file  GS - changed "from load_data import *"
from b_tree import b_tree_files
from main.b_tree_validation import BTreeValidation
from main.b_tree_performance_tests import BTreePerformanceTests
from main.performance_results_logger import PerformanceResultsLogger
from main.key_generator import KeyGenerator

#To fix import errors 
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)  # Insert at beginning so it takes priority

def run_btree_experiment(df, key_attributes, t, results_logger, name=None, reverse = False):
    key_machine = KeyGenerator(*key_attributes)
    sorted_df = sort_by_variousId.sort_by_attribute(df, list(key_attributes), reverse = reverse)
    if not name:
        name = f"{'_'.join(key_attributes)}"
    b_tree = b_tree_files.BTree.create_Btree_from_df(sorted_df, t=t, key_generator=key_machine, name=name)
    b_tree.sorted = not reverse
    key_list = key_machine.get_keys()
    # Validate and test performance
    validator = BTreeValidation(b_tree, key_list)
    validator.validate()
    performance = BTreePerformanceTests(b_tree, key_list).test_all()
    
    # Add the name to the performance record
    performance['tree_name'] = name
    results_logger.log_result(performance)

def run_composite_key_search(prod_df, keys, results_logger, t=9):
# composite key tests only - min deg = 9
    print(f'\n[INFO] Running composite key search for {keys} at degree {t}')
    key_machine = KeyGenerator(*keys)
    sorted_df = sort_by_variousId.sort_by_attribute(prod_df, list(keys))
    b_tree = b_tree_files.BTree.create_Btree_from_df(sorted_df, t=t, key_generator=key_machine, name=f"{'_'.join(keys)}")
    key_list = key_machine.get_keys()
    composite_results = BTreePerformanceTests(b_tree, key_list).test_composite_key_search()
    composite_results['tree_name'] = f"{'_'.join(keys)}_composite_search_demo"
    results_logger.log_result(composite_results)


def main():
    prod_df = load_file.load_file()
    results_logger = PerformanceResultsLogger()   
    composite_keys = [("Merchant ID", "Cluster ID"), ("Cluster ID", "Merchant ID"),
        ("Category ID", "Cluster ID"),("Category Label", "Cluster Label"),]
    if prod_df is None:
       print('Invalid Dataframe')
       return 
    print('[DEBUG]Load Successful\n')
    print('[DEBUG]Columns loaded:', prod_df.columns.tolist()) 

# running with backward sort
    for col in prod_df.columns:
        for min_deg in range(3, 16):
            run_btree_experiment(prod_df, key_attributes=(col,), t=min_deg, results_logger=results_logger, name = None, reverse =True)
    for keys in composite_keys:
        for min_deg in range(3, 16):
            run_btree_experiment(prod_df, key_attributes=keys, t=min_deg, results_logger=results_logger, name = None, reverse  = True)
        run_composite_key_search(prod_df, keys, results_logger, t=9)

# running with forward sort
    for col in prod_df.columns:
        for min_deg in range(3, 16):
            run_btree_experiment(prod_df, key_attributes=(col,), t=min_deg, results_logger=results_logger)
    for keys in composite_keys:
        for min_deg in range(3, 16):
            run_btree_experiment(prod_df, key_attributes=keys, t=min_deg, results_logger=results_logger)
        run_composite_key_search(prod_df, keys, results_logger, t=9)

    # THIS is after we loop through all the trees.
    results_logger.save_to_csv() 
    print(results_logger.get_dataframe().to_string(index=False))

if __name__ == '__main__':
    main()