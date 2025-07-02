import sys
import os
from sort_data import sort_by_variousId
from source_data import load_file #load_file  GS - changed "from load_data import *"
from b_tree import b_tree_files  # was "from b_tree import *"
from main.b_tree_validation import BTreeValidation
from main.b_tree_performance_tests import BTreePerformanceTests
from main.performance_results_logger import PerformanceResultsLogger

#To fix import errors 
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)  # Insert at beginning so it takes priority

def main():
    prod_df = load_file.load_file()
    results_logger = PerformanceResultsLogger()
    if prod_df is None:
       print('Invalid Dataframe')
       return 
    print('[DEBUG]Load Successful\n')
    print('[DEBUG]Columns loaded:', prod_df.columns.tolist()) 
    
    #Create B- Tree for product id 
    #b_tree = b_tree_files2.BTree(5, name= "ProductID", sorted=True)
    key_attribute = "Product ID"
    sorted_df = sort_by_variousId.sort_by_attribute(prod_df, [key_attribute])
    key_list = sorted_df[key_attribute].tolist()    
    b_tree_df = b_tree_files.BTree.create_Btree_from_df(sorted_df,t=5, column_key =key_attribute)

    print("\n--- B-Tree built from DataFrame ---")
    print(f"Root Node: {b_tree_df.root}")
    if not b_tree_df.root.is_leaf:
        print(f"  Root Children: {[str(c) for c in b_tree_df.root.children]}")
        for child in b_tree_df.root.children:
            if not child.is_leaf:
                print(f"    Child Children: {[str(gc) for gc in child.children]}")

    validator = BTreeValidation (b_tree_df, key_list)
    validator.validate()
    performance = BTreePerformanceTests(b_tree_df, key_list).test_all()
    results_logger.log_result(performance)
    
    # THIS is after we loop through all the trees.
    results_logger.save_to_csv() 
    
    # print out a table of the dataframe
    print(results_logger.get_dataframe().to_string(index=False))

if __name__ == '__main__':
    main()