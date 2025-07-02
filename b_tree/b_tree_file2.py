import pandas as pd 
import math 
from sort_data import sort_by_variousId
from source_data import load_file

class Node:
    # t : minimumm dgeree, t-1 key for each node 
    # is_leaf: True if node is a leaf 
    # This B Tree is created with Productid as key 
    def __init__(self, t,is_leaf):
        self.t = t
        self.is_leaf = is_leaf
        self.keys = []       # List to store keys (Product IDs in this case)
        self.children = []   # List to store child nodes (pointers to other binary tree objects)
        self.visits  = 0 # GS added to allow for performance evaluation
        self.record=[] # get records as list to insert in node 
        
        
    def find_key_index(self, key):
        """to find the index where the key should be inserted or where it is found.
        Returns the index `i` such that self.keys[i-1] < key <= self.keys[i].
        """
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        return i

    def split_child(self, i, child_node):
        """
        Splits a full child node (child_node, which is self.children[i]) into two.
        The median key of the child_node is promoted to the current node.
        """
        new_child = Node(self.t, child_node.is_leaf)
        # Insert new_child into self.children after child_node
        self.children.insert(i + 1, new_child)
        # Promote the median key from child_node to current node
        median_key = child_node.keys[self.t - 1] # Index of the median key in a full child_node
        
       
        #median record 
        #median_record = child_node.record[median_key]
        median_record= child_node.record[self.t-1]

        #self.keys.insert(i, child_node.keys[median_key])
        self.keys.insert(i,median_key)
        #insert record 
        #self.keys.insert(i, median_record)
        self.record.insert(i, median_record)

        # Move keys from child_node to new_child
        ''' new_child.keys = child_node.keys[self.t:]
        new_child.records = child_node.record[self.t:]
        child_node.keys = child_node.keys[:self.t - 1] # Child_node retains keys before median
        child_node.records= child_node.record[:self.t-1]'''
        new_child.keys = child_node.keys[self.t:]
        new_child.record = child_node.record[self.t:]

        #use slicing to retain child node keys and records befroe median

        child_node.keys = child_node.keys[:self.t-1]
        child_node.records= child_node.record[:self.t-1]
    

        # If child_node is not a leaf, move children too
        if not child_node.is_leaf:
            new_child.children = child_node.children[self.t:]
            child_node.children = child_node.children[:self.t]

class BTree:
    # tree can have at most 2*t -1 keys and 2*t , order m = 2t 
    # here the key is product id 

    #def __init__(self,t, name = "BTree", sorted=True):
    def __init__(self,t, column_key='id'):
        self.tree = t  # GS - the attribute is called "tree", so we need to access it that way
        self.root = Node(t, True)  # First root entry is leaf 
        self.node_count= 1 
        self.column_key = column_key
        
        #GS - adding some metadata so we can tell which tree is which 
        #self.name = name # a string, so we can name trees.  we probably need to add key name(s)
        #self.sorted = sorted # a boolean to allow us to know if the data was pre-sorted

    @classmethod
    def create_Btree_from_df(cls, df, t, column_key):
        if column_key not in df:
            raise ValueError (f"Key column '{column_key}' not found in DataFrame.")  
        
        b_tree = cls(t, column_key)
        for idx, row in df.iterrows():
            record= row.to_dict()
            b_tree.insert(record)

        return b_tree
   
   
    # Insert keys
    def insert(self, record):
        #fetch key from record
        if self.column_key not in record:
            raise ValueError(f"Record missing key column '{self.column_key}'. Record: {record}")

        # Extract the comparable key from the record
        key = record[self.column_key]
        root_node = self.root
        # increase height if root is full
        if len(root_node.keys) == ((2*self.tree) -1):
             root_new= Node(self.tree, False) # add new root not as leaf
             root_new.children.append(root_node) # old root is not child of new node
             self.root = root_new
             self.node_count+=1
             # split old root and insert key to new root 
             root_new.split_child(0, root_node)
             self.insert_non_full(root_new, record)
        else:
            self.insert_non_full(root_node, record)

    # insert to non-full node 
    def insert_non_full(self, node, record):
        key = record[self.column_key]
        i = node.find_key_index(key)

        if node.is_leaf:
            #node.keys.insert(i, key) # if leaf insert the key directly, commenting this and adding code for records
            #if i < len(node.keys) and node.keys[i]==key:
            #    node.records[i].append(record)
            #else:
            node.keys.insert(i,key)
            node.record.insert(i,record)
        else:
            # If it's an internal node, find the correct child
            child_to_descend = node.children[i]
            # If the child is full, split it before descending
            if len(child_to_descend.keys) == (2 * self.tree - 1):
                node.split_child(i, child_to_descend)
                # After splitting, the key might go into the new child or the current node
                if key > node.keys[i]:
                    i += 1 # Move to the right child if key is greater than the promoted median
                child_to_descend = node.children[i]
                #self.node_count += 1 # A new node was created during split, not required any more
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
            return node.records[i]
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
            for i in range(len(node.keys)):
                if not node.is_leaf:
                    self.inorder_traverse_recursive(node.children[i], result_list)
                result_list.append(node.keys[i])
            if not node.is_leaf:
                self.inorder_traverse_recursive(node.children[len(node.keys)], result_list)



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
            node.visit_count = 0
            for child in node.children:
                reset_node(child)
        reset_node(self.root)

    def get_total_visits(self):
        def count_visits(node):
            count = node.visit_count
            for child in node.children:
                count += count_visits(child)
            return count
        return count_visits(self.root)

        