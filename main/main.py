from sort_data import sort_by_variousId   
from source_data import load_file #load_file  GS - changed "from load_data import *"
from b_tree import b_tree_files # was "from b_tree import *"
from main.b_tree_validation import BTreeValidation
from main.b_tree_performance_tests import BTreePerformanceTests
from main.performance_results_logger import PerformanceResultsLogger

def main():
    prod_df = load_file.load_file()
    results_logger = PerformanceResultsLogger()
    if prod_df is not None: 
       print('[DEBUG]Load Successful\n')
       print('[DEBUG]Columns loaded:', prod_df.columns.tolist()) 

    #Create B- Tree for product id 
    b_tree = b_tree_files.BTree(5, name= "ProductID", sorted=True)
    sorted_df = sort_by_variousId.sort_by_attribute(prod_df, ['Merchant ID', 'Product ID'])
    product_ids = sorted_df['Product ID'].tolist()
    
    for pid in product_ids: # we should try sorted vs unsorted insertion as an experiment later
       b_tree.insert(pid)
    
    # GS - create a bunch of trees
    # GS - do the following for each tree
    validator = BTreeValidation (b_tree, product_ids)
    validator.validate()
    performance = BTreePerformanceTests(b_tree, product_ids).test_all()
    results_logger.log_result(performance)
    
    
    # THIS is after we loop through all the trees.
    results_logger.save_to_csv() 
    
    # print out a table of the dataframe
    print(results_logger.get_dataframe().to_string(index=False))

if __name__ == '__main__':
    main()
