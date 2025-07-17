from flask import Flask, request, render_template
import pandas as pd
from source_data.load_file import load_file
from main.key_generator import KeyGenerator
from b_tree.b_tree_files import BTree
from sort_data.sort_by_variousId import random_sort_by_attribute, sort_by_attribute


app = Flask(__name__)

df = load_file()
columns = df.columns.tolist()
composite_keys = [  ("Merchant ID", "Cluster ID"),  ("Merchant ID", "Category ID")]
btrees = {}
t = 9 # min degree for thse trees
#df = random_sort_by_attribute(df, sort_attributes=["Product ID"]) #adding this to use random insert

# Create trees for single-column keys - set min deg at 9
for col in columns:
    key_machine = KeyGenerator(col)
    name = col.lower().replace(" ", "_")  #needed for URLs
    df = sort_by_attribute(df, sort_attributes=[col]) #adding this to use random insert
    btrees[name] = BTree.create_Btree_from_df(df, t=t, key_generator=key_machine, name=name)

# Create trees for composite keys
for key1, key2 in composite_keys:
    key_machine = KeyGenerator(key1, key2)
    name = f"{key1.lower()}_{key2.lower()}".replace(" ", "_")
    btrees[name] = BTree.create_Btree_from_df(df, t=t, key_generator=key_machine, name=name)

@app.route("/", methods=["GET","POST"])  # need both Get and POST - need GET for initial page load. 
def index():
    result = None
    selected_tree = request.form.get("tree_name", "product_id")
    query = request.form.get("query", "").strip()  #exact match all
    
    range_start = request.form.get("range_start", "").strip()
    range_end = request.form.get("range_end", "").strip() # range search all
    
    start = request.form.get("start", "").strip()

    btree = btrees.get(selected_tree)
    btree.reset_visit_counts()
    
    if not btree:
        result = "Tree not found!"
    elif request.method == "POST":  #i really want to do a case here... I miss java 
        if query:
            result = btree.search_first_match(query) or "No matches found."
        elif range_start and range_end:
            result = btree.range_search(range_start, range_end) or "No matches found."
        elif start:
            result = btree.search_starting_with(start) or "No matches found."
        else:
            result = "Please enter value to search."

    vis = btree.get_total_visits()
    comp = btree.get_total_comparisons()
    return render_template(
        "index.html", 
        result=result,
        trees=btrees.keys(),
        selected_tree=selected_tree,
        visits=vis,
        comparisons=comp
    )

if __name__ == "__main__":
    app.run(debug=True)
