from flask import Flask, make_response, jsonify, request, render_template

app = Flask(__name__)

stock = {
    "fruit": {
        "apple":30,
        "banana":45,
        "cherry":1000
    }
}

# GET
# POST
# PUT
# PATCH
# DELETE

@app.route("/get-text")
def get_text():
    return "some text"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/qs")
def qs():

    if request.args:
        req = request.args
        return " ".join(f"{k}: {v}" for k, v in req.items())
    
    return "No query"



@app.route("/stock")
def get_stock():

    res = make_response(jsonify(stock), 200)

    return(res)


@app.route("/stock/<collection>")
def get_collection(collection):

    #Returns the collection from stock

    if collection in stock:
        res = make_response(jsonify(stock[collection]), 200)
        return res

    res = make_response(jsonify({"error": "Item not found"}), 400)

    return(res)


@app.route("/stock/<collection>/<member>")
def get_member(collection, member):

    #Returns the qty of member

    if collection in stock:
        member = stock[collection].get(member)
        if member:
         res = make_response(jsonify(member), 200)
         return res

    res = make_response(jsonify({"error": "Collection not found"}), 400)

    return(res)


# GET AND POST
@app.route("/add-collection", methods=["GET", "POST"])
def add_collection():

    #If request method is GET = renders a template
    #If request method is POST , and if collections doesnt exist = creates a collection
    

    if request.method == "POST":
        req = request.form

        collection = req.get("collection")
        member = req.get("member")
        qty = req.get("gty")

    
        if collection in stock:
          message = "Collection already exists"
          return render_template("add_collection.html", stock = stock, message = message)
    
        stock[collection] = {member: qty}
        message = "Collection created"

        return render_template("add_collection.html", stock = stock, message = message)

    return render_template("add_collection.html", stock = stock) #this line of code will work when method is GET


# POST=create a collection
@app.route("/stock/<collection>", methods=["POST"])
def create_collection(collection):

    #If collection doesnt exist = creates a new collection

    req = request.get_json()
    
    if collection in stock:
        res = make_response(jsonify({"error": "collection already exists"}), 400)
        return res
    
    stock.update({collection: req})

    res = make_response(jsonify({"message": "collection created"}), 200)
    return res

# PUT a collection
@app.route("/stock/<collection>", methods=["PUT"])
def put_collection(collection):

    #Replaces or creates a  collection. expected body: {"member": qty}

    req = request.get_json()
    
    stock[collection] = req
    
    res = make_response(jsonify({"message": "collection replaced"}), 200)
    return res


# PATCH a collection
@app.route("/stock/<collection>", methods=["PATCH"])
def patch_collection(collection):

    #Updates or creates a  collection. expected body: {"member": qty}

    req = request.get_json()

    if collection in stock:
        for k, v in req.items():
             stock[collection][k] = v
        res = make_response(jsonify({"message": "Collection updated"}), 200)
        return res
    
    stock[collection] = req
    
    res = make_response(jsonify({"message": "collection created"}), 200)
    return res

# DELETE a collection
@app.route("/stock/<collection>", methods=["DELETE"])
def delete_collection(collection):

    #If the collection exists, delete it

    
    if collection in stock:
        del stock[collection]
        res = make_response(jsonify({}), 204)
        return res
    
        
    res = make_response(jsonify({"error": "collection not found"}), 200)
    return res




