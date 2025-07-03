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

def run_btree_experiment(df, key_attributes, t, results_logger, name=None):
    key_machine = KeyGenerator(*key_attributes)
    sorted_df = sort_by_variousId.sort_by_attribute(df, list(key_attributes))
    if not name:
        name = f"{'_'.join(key_attributes)}"
    b_tree = b_tree_files.BTree.create_Btree_from_df(sorted_df, t=t, key_generator=key_machine, name=name)
    key_list = key_machine.get_keys()
    # Validate and test performance
    validator = BTreeValidation(b_tree, key_list)
    validator.validate()
    performance = BTreePerformanceTests(b_tree, key_list).test_all()
    
    # Add the name to the performance record
    performance['tree_name'] = name
    results_logger.log_result(performance)


def main():
    prod_df = load_file.load_file()
    results_logger = PerformanceResultsLogger()
    if prod_df is None:
       print('Invalid Dataframe')
       return 
    print('[DEBUG]Load Successful\n')
    print('[DEBUG]Columns loaded:', prod_df.columns.tolist()) 
    
    for min_deg in range(3, 8):
        for col in prod_df.columns:
            run_btree_experiment(prod_df, key_attributes=(col,), t=min_deg, results_logger=results_logger)


    # GS - these don't work yet
    run_btree_experiment(prod_df, key_attributes=("Merchant ID", "Cluster ID"), t=5, results_logger=results_logger)
#    run_btree_experiment(prod_df, key_attributes = ["Cluster ID", "Merchant ID"], t=min_deg, results_logger=results_logger)
    
    # THIS is after we loop through all the trees.
    results_logger.save_to_csv() 
    print(results_logger.get_dataframe().to_string(index=False))

if __name__ == '__main__':
    main()