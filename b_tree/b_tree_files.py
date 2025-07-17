'''
This version is intended to separate the key, so that it does not have to be 
part of the record
'''
class Node:
    def __init__(self, t, is_leaf):
        self.t = t
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.record = []
        self.visits = 0
        self.comparisons = 0

    def find_key_index(self, key):
        i = 0
        while i < len(self.keys):
            self.comparisons += 1
            if key <= self.keys[i]:
                break
            i += 1
        return i

    def split_child(self, i, child_node):
        new_child = Node(self.t, child_node.is_leaf)
        self.children.insert(i + 1, new_child)
        median_key = child_node.keys[self.t - 1]
        median_record = child_node.record[self.t - 1]
        self.keys.insert(i, median_key)
        self.record.insert(i, median_record)

        new_child.keys = child_node.keys[self.t:]
        new_child.record = child_node.record[self.t:]
        child_node.keys = child_node.keys[:self.t - 1]
        child_node.record = child_node.record[:self.t - 1]

        if not child_node.is_leaf:
            new_child.children = child_node.children[self.t:]
            child_node.children = child_node.children[:self.t]


class BTree:
    def __init__(self, t, name="BTree", sorted=True):
        self.tree = t
        self.root = Node(t, True)
        self.node_count = 1
        self.name = name
        self.sorted = sorted

    @classmethod
    def create_Btree_from_df(cls, df, t, key_generator, name="BTree"):
        b_tree = cls(t, name=name)
        for _, row in df.iterrows():
            record = row.to_dict()
            key = key_generator.generate(record)
            b_tree.insert(key, record)
        b_tree.inorder_traverse()
        return b_tree

    def insert(self, key, record):
        root = self.root
        if len(root.keys) == (2 * self.tree) - 1:
            new_root = Node(self.tree, False)
            new_root.children.append(root)
            self.root = new_root
            self.node_count += 1
            new_root.split_child(0, root)
            self.insert_non_full(new_root, key, record)
        else:
            self.insert_non_full(root, key, record)

    def insert_non_full(self, node, key, record):
        i = node.find_key_index(key)
        if node.is_leaf:
            node.keys.insert(i, key)
            node.record.insert(i, record)
        else:
            child = node.children[i]
            if len(child.keys) == (2 * self.tree - 1):
                node.split_child(i, child)
                if key > node.keys[i]:
                    i += 1
                child = node.children[i]
            self.insert_non_full(child, key, record)

    def search_first_match(self, key):
        self.reset_visit_counts()
        return self._search_first_match(self.root, key)

    def _search_first_match(self, node, key):
        node.visits += 1
        i = node.find_key_index(key)
        if i < len(node.keys) and node.keys[i] == key:
            return node.record[i]  # returning the actual record - since returning the key is just checking for existence
        if node.is_leaf:
            return None  # we didn;t find
        return self._search_first_match(node.children[i], key)

    def search_all_matches(self, key):
        self.reset_visit_counts()
        results = [] # results will eb alist of records
        self._search_all_matches(self.root, key, results)
        return results

    def _search_all_matches(self, node, key, results):
        node.visits += 1
        for i in range(len(node.keys)):
            if not node.is_leaf:
                self._search_all_matches(node.children[i], key, results)
            node.comparisons += 1
            if node.keys[i] == key:
                results.append(node.record[i]) # returning record,
            elif node.keys[i] > key and self.sorted:
                return
        if not node.is_leaf:
            self._search_all_matches(node.children[-1], key, results)

    def range_search(self, key_min, key_max):
        self.reset_visit_counts()
        results = []
        self._range_search(self.root, key_min, key_max, results)
        return results

    def _range_search(self, node, key_min, key_max, results):
        node.visits += 1
        for i in range(len(node.keys)):  #iterate through keys
            if not node.is_leaf:
                self._range_search(node.children[i], key_min, key_max, results)
            node.comparisons += 1
            if key_min <= node.keys[i] <= key_max:
                results.append(node.record[i])
            elif node.keys[i] > key_max and self.sorted:
                return
        if not node.is_leaf:
            self._range_search(node.children[-1], key_min, key_max, results)
            
    def search_starting_with(self, start):
        self.reset_visit_counts()
        results = []
        self._search_starting_with(self.root, start, results)
        return results

    def _search_starting_with(self, node, start, results):
        node.visits += 1
        for i in range(len(node.keys)):
            if not node.is_leaf:
                self._search_starting_with(node.children[i], start, results)
            node.comparisons += 1
            if node.keys[i].startswith(start):
                results.append(node.record[i])
            elif node.keys[i] > start and self.sorted:
                return
        if not node.is_leaf:
            self._search_starting_with(node.children[-1], start, results)
            
    def search_composite(self, key_1=None, key_2=None):
        self.reset_visit_counts()
        results = []
        mode = 2 if key_1 and key_2 else (1 if key_2 else 0)
        if mode == 0: search_key = key_1
        elif mode == 1: search_key = key_2
        else: search_key = f'{key_1} - {key_2}'
        self._search_composite(self.root, search_key, mode, results)
        return results


    def _search_composite(self, node, search_key, mode, results):
        node.visits += 1
        for i in range(len(node.keys)):
            if not node.is_leaf:
                self._search_composite(node.children[i], search_key, mode, results)
            node.comparisons += 1
            key = node.keys[i]
            if mode in (0, 2):  # Modes 0 and 2: stop if first part exceeds search_key
                first_part = key.split(' - ', 1)[0]
                if (mode == 2 and key == search_key) or (mode == 0 and first_part == search_key):
                    results.append(node.record[i])
                elif first_part > search_key and self.sorted:
                    return
            else:
                parts = key.split(' - ', 1)
                if len(parts) > 1 and parts[1] == search_key:
                    results.append(node.record[i])
                    ## this ended up being more complicated that i thought.

        if not node.is_leaf:
            self._search_composite(node.children[-1], search_key, mode, results)

    def inorder_traverse(self):
        result = []
        self.node_count = 0
        self._inorder_traverse_recursive(self.root, result)
        return result

    def _inorder_traverse_recursive(self, node, result_list):
        if node:
            node.visits += 1
            self.node_count +=1
            for i in range(len(node.keys)):
                if not node.is_leaf:
                    self._inorder_traverse_recursive(node.children[i], result_list)
                result_list.append(node.record[i])
            if not node.is_leaf:
                self._inorder_traverse_recursive(node.children[-1], result_list)

    def get_height(self):
        height = 0
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
            height += 1
        return height

    def reset_visit_counts(self):
        def reset_node(n):
            n.visits = 0
            n.comparisons = 0
            for c in n.children:
                reset_node(c)
        reset_node(self.root)

    def get_total_visits(self):
        def count_visits(n):
            return n.visits + sum(count_visits(c) for c in n.children)
        return count_visits(self.root)

    def get_total_comparisons(self):
        def count_comparisons(n):
            return n.comparisons + sum(count_comparisons(c) for c in n.children)
        return count_comparisons(self.root)
