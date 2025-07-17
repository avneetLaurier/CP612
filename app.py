from flask import Flask, request, render_template
import pandas as pd
from source_data.load_file import load_file
from main.key_generator import KeyGenerator
from b_tree.b_tree_files import BTree

app = Flask(__name__)

df = load_file()
columns = df.columns.tolist()
composite_keys = [  ("Merchant ID", "Cluster ID"),  ("Merchant ID", "Category ID")]
btrees = {}
t = 9 # min degree for thse trees

# Create trees for single-column keys - set min deg at 9... or per experiment results
for col in columns:
    key_machine = KeyGenerator(col)
    name = col.lower().replace(" ", "_")  #needed for URLs
    btrees[name] = BTree.create_Btree_from_df(df, t=t, key_generator=key_machine, name=name)

# Create trees for composite keys
for key1, key2 in composite_keys:
    key_machine = KeyGenerator(key1, key2)
    name = f"{key1.lower()}_{key2.lower()}".replace(" ", "_")
    btrees[name] = BTree.create_Btree_from_df(df, t=t, key_generator=key_machine, name=name)

@app.route('/test')
def test():
    return render_template('index.html', trees=["T1"], selected_tree=None, result=None)

@app.route("/", methods=["GET","POST"])  # need both Get and POST - need GET for initial page load. 
def index():
    result = None
    selected_tree = request.form.get("tree_name", "product_id")
    query = request.form.get("query", "").strip()
    range_start = request.form.get("range_start", "").strip()
    range_end = request.form.get("range_end", "").strip()
    prefix = request.form.get("prefix", "").strip()

    btree = btrees.get(selected_tree)
    if not btree:
        result = "Invalid tree selected."
    elif request.method == "POST":
        if query:
            result = btree.search_all_matches(query) or "No matches found."
        elif range_start and range_end:
            result = btree.range_search(range_start, range_end) or "No matches found in range."
        elif prefix:
            result = btree.search_starting_with(prefix) or "No matches found for prefix."
        else:
            result = "Please enter a search value."

    return render_template("index.html", result=result, trees=btrees.keys(), selected_tree=selected_tree)

if __name__ == "__main__":
    app.run(debug=True)
