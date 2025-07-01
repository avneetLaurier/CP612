class BTreeValidation:
    def __init__(self, b_tree,key_list):
        self.b_tree = b_tree
        self.key_list = key_list
        
    def tree_stats(self):
        # Display B-Tree properties
        t = self.b_tree.tree
        print("\n--- B-Tree Statistics ---")
        print(f"B-Tree Minimum Degree (t): {t}")
        print(f"Maximum keys per node: {2 * t - 1}")
        print(f"Minimum keys per non-root node: {t - 1}")
        print(f"Total entries inserted: {len(self.key_list)}")
        print(f"Number of nodes in the B-Tree: {self.b_tree.node_count}")
        print(f"Height of the B-Tree: {self.b_tree.get_height()} (root at level 0)")

    def verify_sorting(self):
        # Verify sorting (by traversing)
        print("\n--- Verifying B-Tree Order (First 20 and Last 20 keys via traversal) ---")
        traversed_keys = self.b_tree.inorder_traverse()  
        print("First 20 traversed keys:", traversed_keys[:20])
        print("Last 20 traversed keys:", traversed_keys[-20:])
        print(f"Is the traversed list sorted? {traversed_keys == sorted(self.key_list)}")

    def test_search(self):    
        # Test search functionality
        print("\n--- Testing Search ---")
        search_key_1 = self.key_list[len(self.key_list) // 2] # A key that should exist
        if isinstance (search_key_1, int):
            search_key_2 = 999999999 # A key that should not exist
        else:
            search_key_2 = "STRING_TEST_KEY"

        found_node_1 = self.b_tree.search(search_key_1)
        if found_node_1:
            print(f"Search for {search_key_1}: Found (in node with keys: {found_node_1.keys})")
        else:
            print(f"Search for {search_key_1}: Not Found")

        found_node_2 = self.b_tree.search(search_key_2)
        if found_node_2:
            print(f"Search for {search_key_2}: Found (in node with keys: {found_node_2.keys})")
        else:
            print(f"Search for {search_key_2}: Not Found")
            
    def validate (self):
        self.tree_stats()
        self.verify_sorting()
        self.test_search() 


