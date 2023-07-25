from flask import Flask , request ,jsonify,render_template,url_for , session , redirect ,json 
from werkzeug.security import generate_password_hash, check_password_hash 
from dotenv import dotenv_values 
from werkzeug.exceptions import HTTPException
import jwt 

CONFIG = dotenv_values(".env") 

app = Flask(__name__) 

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

# @app.before_request

# def before_caller():
#     return "Runs Always before all requests handlers"

@app.route("/" , methods=["GET"])
def index_handler():
    # return "Welcome to Flask Lesson" 
    return render_template(
        "index.html" , 
        author = "Adeleke Bright" ,
        colors = ["Red" , "Blue" , "Yellow"]        
    )

@app.route("/examples/basic" , methods=["GET"])
def basic_path():
    return "Hello,World"

@app.route("/examples/json" , methods=["GET"])
def json_path():
    ''' Shows how to return a json response '''
    return jsonify({
        "message": "This is a json path",
        "success" : True,
        "data" : []
    }) , 200

@app.route("/examples/templates" , methods=["GET"])
def template_handler():
    return render_template(
        "example.html" , 
        title = "Example Template",
        services =  ["Coaching" , "Consultancy" , "Research"] ,
        validUser =  {
            "name" : "Adeleke Bright"
        }
    )

# Create a contact page for handling contact us 

@app.route("/contact" , methods=["GET" , "POST"])
def contact_handler():
    if request.method == "GET":
        return render_template(
            "contact.html",
            title = "Contact us" 
        )
    
    elif request.method == "POST":
        username = request.form.get("name") 
        email = request.form["email"] 
        message = request.form.get("message")
        file = request.files["attachment"] 
        if file:
            storagePath = "./temp/" + file.filename 
            file.save(storagePath)
        return jsonify({
            "success" : True , 
            "data" : {
                "message" : message , 
                "username" : username,
                "email":email
            },
            "message" : "We will get in touch with you"
        }) ,201

# Handling Query String 
@app.route("/search" , methods=["GET"]) 
def search_handler():
    value = request.args.get("q")
    return jsonify({
        "success"  :True ,
        "message" : "You are searching for {}".format(value)
    }),200

#Handle File Upload 
@app.route("/upload" , methods=["GET" , "POST"])
def upload_handler():
    if request.method == "GET":
        return render_template(
            "upload.html",
            title = "File Upload" 
        )
    
    elif request.method == "POST":
        f = request.files["profile"] 
        filePath = "./temp/" + f.filename
        f.save(filePath)

        return jsonify({
            "success" : True , 
            "message" : "Your file was successfully uploaded"
        }) ,201
    
#We want to leverage python's list and dictionary for adding, updating, deleting, and get 
users = [] 

@app.route("/users" , methods=["GET" , "POST"]) 
def users_handler():
    if request.method == "GET":
        message =  "Users retrieved" if len(users) > 0  else  "No user found"
        return jsonify({
            "message" : message , 
            "status" : True , 
            "data" : users , 
            "statusCode" : 200
        })
    
    elif request.method == "POST":
        request_body = request.get_json() 

        name = request_body["name"] 
        email = request_body["email"] 
        age = request_body["age"] 

        user = {
            "id" : len(users) + 1 ,
            "name" : name ,
            "email" : email , 
            "age" : age
        }

        users.append(user)

        # return "We are yet to implement it"
        return jsonify({
            "message" : "User was added successfully" , 
            "status" : True , 
            "data" : users , 
            "statusCode" : 201
        }) , 201 
    

def get_user(id):
    user_hash = {}
    for user in users:
        if user["id"] == id :
            user_hash = user
    
    return user_hash
@app.route("/users/<int:id>" , methods=["GET" , "DELETE" , "PUT"]) 
def user_handler(id):
    if request.method == "GET":
        user_hash = get_user(id)
        return jsonify(user_hash)

    elif request.method =="DELETE":
        return "Not Implemented delete yet"
    
    elif request.method =="PUT":
        return "Not Impelemted put yet"

# Handle Redirection, Session, and Authentication using a basic sign up flow 

@app.route("/auth/sign-up" , methods=["POST"])
def registration_handler():
    return "Registration"

@app.route("/auth/login" , methods=["GET" , "POST"])
def login_handler():
    password = request.args.get("password") 
    if not password :
        return "Please provide password "
    
    hash_password = generate_password_hash(password) 
    print(password , hash_password)
    # Now, compare the passwords 
    valid_password = "12345678" 
    if not check_password_hash(hash_password , valid_password):
        return "Password is not correct"
    
    name = "Jason Statham"
    return redirect(url_for("dashboard_handler" , name=name))

@app.route("/dashboard/<name>" , methods=["GET"])

def dashboard_handler(name):
    session_count = session.get("count") if session.get("count") else 0 
    count = session_count + 1
    #session.pop("count" , None)
    session["count"] = count 

    return "Welcome {}. Count is {}".format(name , count)

#Working with JWT Token 

@app.route("/token" , methods=["GET"])
def token_generator():
    payload = {
        "name" : "John Mahama" , 
        "email" : "bola@gmail.com"
    } 

    token = jwt.encode(payload , "secret") 

    return jsonify({
        "token" : token 
    }) , 200

@app.route("/decode-token" , methods=["GET"])
def token_handler():
    auth = request.headers.get("Authorization") 
    if not auth :
        return jsonify({
            "message" : "Missing Authorization Header"
        }),401
    auth_list = auth.split(" ") 
    if auth_list[0] != "Bearer" or not auth_list[1]:
        return jsonify({
            "message" : "Bad Auth"
        }),400
    token = auth.split(" ")[1]
    decoded  = jwt.decode(token, "secret" , ["HS256"]) 
    if not decoded:
          return jsonify({
            "message" : "Could not decode the token"
        }),500
    return jsonify({
        "success" :True
    }) , 200

if __name__ == "__main__":

    debug = True 

    app.secret_key= CONFIG.get("APP_SECRET")
    app.run(CONFIG.get("HOST") , int(CONFIG.get("PORT")) , debug)
   