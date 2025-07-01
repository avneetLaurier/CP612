# /main/b_tree_tests.py

class BTreePerformanceTests:
    def __init__(self, b_tree, key_list):
        self.b_tree = b_tree
        self.key_list = key_list

    def test_exact_search(self, sample_keys):
        print("\n[Test] Exact Search")  
        # insert logic here
        print(f"Total node visits: {self.b_tree.get_total_visits()}")

    def test_range_search(self, key_min, key_max):
        print(f"\n[Test] Range Search from {key_min} to {key_max}")
        # insert logic here
        print(f"Total node visits: {self.b_tree.get_total_visits()}")

    def test_all(self):
        print("\n--- Performance Test ---")
        # print key or key names (column)
        # print min degree, order and depth
        # print sorted or unsorted? 
        # run all tests


