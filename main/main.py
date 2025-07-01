from sort_data import sort_by_variousId
from source_data import load_file #load_file  GS - changed "from load_data import *"
from b_tree import b_tree_files # was "from b_tree import *"
from main.b_tree_validation import BTreeValidation

def main():
    prod_df = load_file.load_file()
    if prod_df is not None: 
       print('[DEBUG]Load Successful\n')
       print('[DEBUG]Columns loaded:', prod_df.columns.tolist()) 
       productid_sort = sort_by_variousId.sort_by_productid(prod_df)
       product_ids = productid_sort['Product ID'].tolist()

    #Create B- Tree for product id 
    b_tree = b_tree_files.BTree(5, name= "ProductID", sorted=True)
    for pid in product_ids: # we should try sorted vs unsorted insertion as an experiment later
       b_tree.insert(pid)
    
    validator = BTreeValidation (b_tree, product_ids)
    validator.validate()


''' <- moved to separate class, to keep code tight.
    # Display B-Tree properties
    print("\n--- B-Tree Statistics ---")
    print(f"B-Tree Minimum Degree (t): {b_tree.tree}")
    print(f"Maximum keys per node: {2 * b_tree.tree - 1}")
    print(f"Minimum keys per non-root node: {b_tree.tree - 1}")
    print(f"Total entries inserted: {len(product_ids)}")
    print(f"Number of nodes in the B-Tree: {b_tree.node_count}")
    print(f"Height of the B-Tree: {b_tree.get_height()} (root at level 0)")


    # Verify sorting (by traversing)
    print("\n--- Verifying B-Tree Order (First 20 and Last 20 keys via traversal) ---")
    traversed_keys = b_tree.inorder_traverse()  #updated function name - i didn't see a "traverse" function
    print("First 20 traversed keys:", traversed_keys[:20])
    print("Last 20 traversed keys:", traversed_keys[-20:])
    print(f"Is the traversed list sorted? {traversed_keys == sorted(product_ids)}")


    # Test search functionality
    print("\n--- Testing Search ---")
    search_key_1 = product_ids[len(product_ids) // 2] # A key that should exist
    search_key_2 = 999999999 # A key that should not exist

    found_node_1 = b_tree.search(search_key_1)
    if found_node_1:
        print(f"Search for {search_key_1}: Found (in node with keys: {found_node_1.keys})")
    else:
        print(f"Search for {search_key_1}: Not Found")

    found_node_2 = b_tree.search(search_key_2)
    if found_node_2:
        print(f"Search for {search_key_2}: Found (in node with keys: {found_node_2.keys})")
    else:
        print(f"Search for {search_key_2}: Not Found")
'''

if __name__ == '__main__':
    main()