from app import app

from flask import render_template, request, redirect, jsonify, make_response, abort

from datetime import datetime

import os

from werkzeug.utils import secure_filename


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/")
def index():

    # app.config["SECRET_KEY"] = "secret_key"

    # app.config["DB_USERNAME"]="root"

    # print (app.config["DB_USERNAME"])

    # print(app.config["ENV"])

    # print (f"FLASK ENV is set to : {app.config['ENV']}")
    abort(500)
    
    return render_template("public/index.html")

@app.route("/jinja")
def jinja():

    my_name = "Paul"

    age=27

    langs= ["Python", "Java", "Javascript", "Ruby"]

    friends = {
        "Tom":30,
        "Helen":25,
        "Mina":28,
        "John":40
    }

    colours = {"Red","Blue"}

    cool = True
       
    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pulling repo {self.name}"
        
        def clone(self):
            return f"Cloning into {self.url}"
        
    
    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template design tutorial",
        url="https://github.com/vsgitdev")
        


    def repeat(x, qty):
        return x * qty
    
    date = datetime.utcnow()

    my_html = "<h1>THIS IS SOME HTML</h1>"

    suspicious = "<script>alert('you got hacked')</script>"
        
    return render_template(
        "public/jinja.html", my_name=my_name, age=age,
        langs=langs, friends=friends, colours=colours, 
        cool=cool, GitRemote=GitRemote, repeat=repeat,
        my_remote=my_remote, date=date, my_html=my_html,
        suspicious=suspicious
        )



@app.route("/about")
def about():
    return render_template("public/about.html")


# @app.route("/sign-up", methods=["GET", "POST"])
# def sign_up():
#     if request.method == "POST":

#        req = request.form

#        username = req["username"]
#        email = req.get("email")
#        password = request.form["password"]

#        print(username, email, password)

#        return redirect(request.url)

#     return render_template("public/sign_up.html")


users ={
    "mitsuhiko":{
        "name":"Armin Ronacher",
        "bio":"Creator of the Flask Framework",
        "twitter_handle":"@mitsuhiko"
    },
     "elonmusk":{
        "name":"Elon Musk",
        "bio":"technology entrepreneur, ivestor, and engineer",
        "twitter_handle":"@elonmusk"
    },
     "gvanrossum":{
        "name":"Guido Van Rossum",
        "bio":"Creator of the Python programming language",
        "twitter_handle":"@gvanrossum"
    }
}



# @app.route("/profile/<username>")
# def profile(username):


#     user = None

#     if username in users: 
#         user = users[username]

#     return render_template("public/profile.html", username=username, user=user)




@app.route("/multiple/<foo>/<bar>/<baz>")
def multi(foo, bar, baz):
    return f"foo is {foo}, bar is {bar} and baz is {baz}"

@app.route("/json", methods=["POST"])
def json():

    if request.is_json:

      req = request.get_json()

      response = {
         "message" : "JSON received",
         "name": req.get("name")
        }

      res = make_response(jsonify(response), 200)

      return res
    
    else:

        res = make_response(jsonify({"message": "No JSON received"}), 400)
        return res
    

@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create_entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res


@app.route("/query")
def query():

    print(request.query_string)

    return "No query received", 200

app.config["IMAGE_UPLOADS"] = "C:\\Users\\user\\app\\app\\static\\img\\uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

def allowed_image(filename):

    if not "." in filename :
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
    

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False



@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST" :

        if request.files:

            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("file exceeded maximum size")
                return redirect(request.url)
            
            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image saved")

            return redirect(request.url)

    return render_template("public/upload_image.html")


from flask import send_from_directory, abort

"""
string:
int:
float:
path:
uuid:
"""

app.config["CLIENT_IMAGES"] = r"C:\Users\user\app\app\static\client\img"
app.config["CLIENT_CSV"] = r"C:\Users\user\app\app\static\client\csv"
app.config["CLIENT_REPORTS"] = r"C:\Users\user\app\app\static\client\reports"


@app.route("/get-image/<string:image_name>")
def get_image(image_name):

    # print(type(image_name))

    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"],filename=image_name, as_attachment=True)    
    except FileNotFoundError:
        abort(404)



@app.route("/get-csv/<filename>")
def get_csv(filename):

    
    try:
        return send_from_directory(
            app.config["CLIENT_CSV"],filename=filename, as_attachment=True)    
    except FileNotFoundError:
        abort(404)


@app.route("/get-report/<path:path>")
def get_report(path):

    
    try:
        return send_from_directory(
            app.config["CLIENT_REPORT"],filename=path, as_attachment=True)    
    except FileNotFoundError:
        abort(404)


from flask import request, make_response

@app.route("/cookies")
def cookies():

    res = make_response("cookies", 200)

    cookies = request.cookies

    flavor = cookies.get("flavor")
    choc_type = cookies.get("chocolate flavor")
    chewy = cookies.get("chewy")


    print(flavor, choc_type, chewy)

    res.set_cookie(
        "flavor", 
        value ="chocolate flavor",
        max_age = 10,
        expires = None,
        path = request.path,
        domain =  None,
        secure = True,
        httponly = False,
        samesite ='Lax'
        )
    

    res.set_cookie("chocolate type","dark")
    res.set_cookie("chewy","yes")

    return res
    

# only for session demonstration, without security
from flask import render_template, request, session, redirect, url_for

app.config["SECRET_KEY"]='GkkPGqiwuKfB01LRgV3KHA'

users = {
    "julian": {
        "username" : "julian",
        "email" : "julain@example.com",
        "password" : "example",
        "bio" : "random internet guy"
    },
    "clarissa": {
        "username" : "clarissa",
        "email" : "clarissa@example.com",
        "password" : "sweetpotato22",
        "bio" : "Sweet potato is life"
    }
}

@app.route("/sign-in", methods=["GET","POST"])
def sign_in():

    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")

        if not username in users:
            print("username not found")
            return redirect(request.url)
        else:
            user = users[username]
        
        if not password == user["password"]:
            print("password incorrect")
            return redirect(request.url)
        
        else:
            session["USERNAME"] = user["username"]
            print(session)
            print ("user added to session")
            return redirect(url_for("profile"))

    return render_template("public/sign_in.html")

# !!!!!!!!!!!!!!!!!! Dont put any sensitive info into session because: !!!!!!!!!!!!!!!!!!!!!!!

# session=eyJVU0VSTkFNRSI6Imp1bGlhbiJ9.ZuHxFA.VKN6PPENfpO1dbPuaOOlwRDBbA8; HttpOnly; Path=/
# b'{"USERNAME":"julian"}f\xe1\xf1\x14\x05J7\xa3\xcf\x10\xd7\xe9;W[>\xe6\x8e:\\\x11\x0c\x16\xc0\xf0{m\xa4\xe9\xe5\xc8\xf6\xad'

# eyJQQVNTV09SRCI6ImV4YW1wbGUiLCJVU0VSTkFNRSI6Imp1bGlhbiJ9.ZuHy6Q.DUE83ck8Yr0uL1ORhIjd3hrwzSA; HttpOnly; P
# Terminal >>> base64.b64decode("eyJQQVNTV09SRCI6ImV4YW1wbGUiLCJVU0VSTkFNRSI6Imp1bGlhbiJ9.ZuHy6Q.DUE83ck8Yr0uL1ORhIjd3hrwzSA; HttpOnly; Pat")
# b'{"PASSWORD":"example","USERNAME":"julian"}f\xe1\xf2\xe9\x00\xd4\x13\xcd\xdc\x93\xc6+\xd2\xe2\xf59\x18H\x8d\xdd\xe1\xaf\x0c\xd2\x00{m\xa4\xe9\xe5\xc8\xf6\xad'

# (hold only uid in session)


@app.route("/profile")
def profile():

    if session.get("USERNAME", None) is not None:
        username = session.get('USERNAME')
        user = users[username]
        return render_template("public/profile.html", user=user)
    else:
        print("Username not found in session")
        return redirect(url_for("sign_in"))
    

@app.route("/sign-out")
def sign_out():

    session.pop("USERNAME", None)

    return redirect(url_for("sign_in"))


from flask import flash

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
      
    if request.method == "POST":

       req = request.form

       username = req.get("username")
       email = req.get("email")
       password = req.get("password")

       if not len(password) >= 10:
           flash("Password must be at least 10 characters in length", "danger")
           return redirect(request.url)           

       flash("Account created!", "success")
       return redirect(request.url)

    return render_template("public/sign_up.html")
    







