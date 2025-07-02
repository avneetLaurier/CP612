import sys
import os

#To fix import errors 
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)  # Insert at beginning so it takes priority


from sort_data import * #sort_by_variousId
from source_data import load_file #load_file  GS - changed "from load_data import *"
from b_tree import b_tree_file2  # was "from b_tree import *"
from main.b_tree_validation import BTreeValidation

def main():
    prod_df = load_file.load_file()
    if prod_df is not None: 
       print('[DEBUG]Load Successful\n')
       print('[DEBUG]Columns loaded:', prod_df.columns.tolist()) 
       productid_sort = sort_by_productid(prod_df)
       product_ids = productid_sort['Product ID'].tolist()

    #Create B- Tree for product id 
    #b_tree = b_tree_files2.BTree(5, name= "ProductID", sorted=True)
    b_tree_df = b_tree_file2.BTree.create_Btree_from_df(productid_sort,t=5, column_key ='Product ID')

    print("\n--- B-Tree built from DataFrame ---")
    print(f"Root Node: {b_tree_df.root}")
    if not b_tree_df.root.is_leaf:
        print(f"  Root Children: {[str(c) for c in b_tree_df.root.children]}")
        for child in b_tree_df.root.children:
            if not child.is_leaf:
                print(f"    Child Children: {[str(gc) for gc in child.children]}")

    '''for pid in productid_sort: #product_ids: # we should try sorted vs unsorted insertion as an experiment later
       b_tree.insert(pid)'''
    
    '''for  pid, row in product_ids,productid_sort.iterrows():
        #key = row['Product ID']  # 
        #key = 
        record = row.to_dict()
        #b_tree.insert(key,record)
        b_tree.insert(pid, record)'''
    
    validator = BTreeValidation (b_tree_df, product_ids)
    validator.validate()


if __name__ == '__main__':
    main()