import pickle

# we are going to use the Flask micro web framework
from flask import Flask, request, jsonify

app = Flask(__name__)


def load_model():
    infile = open("tree.p", "rb")
    header, tree = pickle.load(infile)
    infile.close()
    return header, tree


def tdidt_predict(header, tree, instance):
    info_type = tree[0]
    if info_type == "Leaf":
        return tree[1] # label
    att_index = header.index(tree[1])
    for i in range(2, len(tree)):
        value_list = tree[i]
        if value_list[1] == instance[att_index]:
            return tdidt_predict(header, value_list[2], instance)
        
# we need to add some routes
# a route is a function that handles a request
# eg for the html content for a home page
# or for the JSON response for a /predict API endpoint, etc
@app.route("/")
def index():
    return"<h1>Welcome to the interview predictor app</h1>", 200

@app.route("/predict")
def predict():
    level = request.args.get("level")
    lang = request.args.get("lang")
    tweets = request.args.get("tweets")
    phd = request.args.get("phd")
    instance = [level, lang, tweets, phd]
    header, tree = load_model()
    pred = tdidt_predict(header, tree, instance)
    if pred is not None:
        return jsonify({"prediction": pred}), 200
    return "Error making a predicition", 400

if __name__ == "__main__":
    # header, tree = load_model()
    # print(header)
    # print(tree)
    app.run(host="0.0.0.0", port=5000, debug=False)
    # TODO: when depoloying an app to prod, set debug to false
    # and check host and port vals