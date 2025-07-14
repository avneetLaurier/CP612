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


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_tree = request.form.get("tree_name", "product_id")  # default tree
    query = request.form.get("query", "").strip()

    if request.method == "POST" and query:
        btree = btrees.get(selected_tree)
        if not btree:
            result = "Invalid tree selected."
        else:
            matches = btree.search_all_matches(query)
            result = matches if matches else "No matches found."

    return render_template("index.html", result=result, trees=btrees.keys(), selected_tree=selected_tree)

if __name__ == "__main__":
    app.run(debug=True)
