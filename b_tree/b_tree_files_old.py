import pandas as pd 
from sort_data import sort_by_variousId
from source_data import load_file

class Node:
    def __init__(self, t,is_leaf):
        self.t = t
        self.is_leaf = is_leaf
        self.keys = []       # List to store keys
        self.children = []   # List to store child nodes 
        self.visits  = 0 # GS added to allow for performance evaluation
        self.record=[] # get records as list to insert in node     
        
    def find_key_index(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        return i

    def split_child(self, i, child_node):
        new_child = Node(self.t, child_node.is_leaf)
        # Insert new_child into self.children after child_node
        self.children.insert(i + 1, new_child)
        # Promote the median key from child_node to current node
        median_key = child_node.keys[self.t - 1] # Index of the median key in a full child_node
        median_record= child_node.record[self.t-1]
        # median_key = self.t - 1    GS - this is the old code. Looks wrong , but somehow worked? 
        self.keys.insert(i, median_key)
        self.record.insert(i, median_record)
        # Populate keys & records in 2 child nodes - GS nice use of slicing!
        new_child.keys = child_node.keys[self.t:]
        new_child.record = child_node.record[self.t:]
        child_node.keys = child_node.keys[:self.t - 1]
        child_node.records= child_node.record[:self.t-1]
        
        # If child_node is not a leaf, move children too
        if not child_node.is_leaf:
            new_child.children = child_node.children[self.t:]
            child_node.children = child_node.children[:self.t]

class BTree:
    # tree can have at most 2*t -1 keys and 2*t , order m = 2t 
    # here the key is product id 

    def __init__(self,t, column_key="Product ID", name = "BTree", sorted=True):
        self.tree = t  # GS - the attribute is called "tree", so we need to access it that way
        self.root = Node(t, True)  # First root entry is leaf 
        self.node_count= 1 
        self.column_key = column_key
        self.name = name # a string, so we can name trees.  we probably need to add key name(s)
        self.sorted = sorted # a boolean to allow us to know if the data was pre-sorted
    
    @classmethod
    def create_Btree_from_df(cls, df, t, column_key):
        if column_key not in df:
            raise ValueError (f"Key column '{column_key}' not found in DataFrame.")
        b_tree = cls(t, column_key)
        for idx, row in df.iterrows():
            record= row.to_dict()
            b_tree.insert(record)
        return b_tree
        
    def insert(self, record):
        #fetch key from record - GS - I dont think we need this for this dataset
        if self.column_key not in record:
            raise ValueError(f"Record missing key column '{self.column_key}'. Record: {record}")
        root_node = self.root
        # increase height if root is full
        if len(root_node.keys) == ((2*self.tree) -1):
             root_new= Node(self.tree, False) # add new root not as leaf
             root_new.children.append(root_node) # old root is not child of new node
             self.root = root_new
             self.node_count+=1
             # split old root and insert record to new root 
             root_new.split_child(0, root_node)
             self.insert_non_full(root_new, record)
        else:
            self.insert_non_full(root_node, record)

    # insert to non-full node 
    def insert_non_full(self, node, record):
        key = record[self.column_key]
        i = node.find_key_index(key)

        if node.is_leaf:
            node.keys.insert(i,key)
            node.record.insert(i,record)
        else:
            # If it's an internal node, find the correct child
            child_to_descend = node.children[i]
            # If the child is full, split it before descending
            if len(child_to_descend.keys) == (2 * self.tree - 1):
                node.split_child(i, child_to_descend)
                if key > node.keys[i]:
                    i += 1 # Move to the right child if key is greater than the promoted median
                child_to_descend = node.children[i]
            self.insert_non_full(child_to_descend,record)

    #Search for key in in Binary- Tree
    def search(self, key):
        return self.search_recursive(self.root, key)

    # Recursive search 
    def search_recursive(self, node, key):
        if node is None: # corrected "Node" to "node"
            return None # key not found 
        node.visits +=1
        i = node.find_key_index(key)

        # if key in current node 
        if i< len(node.keys) and node.keys[i] ==key:
            return node
        elif node.is_leaf:
            return None
        else:
            return self.search_recursive(node.children[i], key)
        
    
    def inorder_traverse(self):
        result=[]
        self.inorder_traverse_recursive(self.root, result)
        return result
    
    # recursive inorder traversal
    def inorder_traverse_recursive(self, node, result_list):
        if node: 
            node.visits += 1
            for i in range(len(node.keys)):
                if not node.is_leaf:
                    self.inorder_traverse_recursive(node.children[i], result_list)
                result_list.append(node.keys[i])
            if not node.is_leaf:
                self.inorder_traverse_recursive(node.children[len(node.keys)], result_list)

# GS added an efficient non-full traversal search that returns multiple keys IF btree is sorted.
    def search_all_matches_sorted(self, key):
        self.reset_visit_counts()
        return self.search_all_matches_recursive(self.root, key, found=False)

    def search_all_matches_recursive(self, node, key, found):
        matches = []
        if node is None:
            return matches
        node.visits += 1
        for i in range(len(node.keys)):
            if not node.is_leaf:
                child_matches = self.search_all_matches_recursive(node.children[i], key, found)
                matches.extend(child_matches)
                if child_matches:
                    found = True  
            if node.keys[i] == key:
                matches.append(node.keys[i])
                found = True
            elif found and node.keys[i] > key:
                return matches  # Since sorted, no further matches will exist
        if not node.is_leaf:
            child_matches = self.search_all_matches_recursive(node.children[len(node.keys)], key, found)
            matches.extend(child_matches)
        return matches


    def get_height(self):
        """Calculates the height (depth) of the B-tree."""
        height = 0
        current_node = self.root
        while not current_node.is_leaf:
            height += 1
            if current_node.children: # Only proceed if it has children
                current_node = current_node.children[0] # Go down left-most child
            else: # Should not happen in a valid B-tree if not leaf and no children
                break
        return height    
    
    def reset_visit_counts(self): #GS - sets all nodes to 0
        def reset_node(node):
            node.visits = 0
            for child in node.children:
                reset_node(child)
        reset_node(self.root)

    def get_total_visits(self):
        def count_visits(node):
            count = node.visits
            for child in node.children:
                count += count_visits(child)
            return count
        return count_visits(self.root)

        