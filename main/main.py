import sort_by_variousId
import  sort_data.sort_by_variousId
from load_file import * #load_file
from b_tree import *

def main():
    b_tree = b_tree.b_tree_files.BTree(5)
    pd = load_file()
    if pd is not None: 
     productid_sort = sort_by_variousId.sort_by_productid()
     product_ids = productid_sort['Product ID'].tolist()

    #Create B- Tree for product id 
    for pid in productid_sort:
       b_tree.insert(pid)


    # Display B-Tree properties
    print("\n--- B-Tree Statistics ---")
    print(f"B-Tree Minimum Degree (t): {b_tree.t}")
    print(f"Maximum keys per node: {2 * b_tree.t - 1}")
    print(f"Minimum keys per non-root node: {b_tree.t - 1}")
    print(f"Total entries inserted: {len(product_ids)}")
    print(f"Number of nodes in the B-Tree: {b_tree.node_count}")
    print(f"Height of the B-Tree: {b_tree.get_height()} (root at level 0)")


    # Verify sorting (by traversing)
    print("\n--- Verifying B-Tree Order (First 20 and Last 20 keys via traversal) ---")
    traversed_keys = b_tree.traverse()
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

if __name__ == '__main__':
    main()