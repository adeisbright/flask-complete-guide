from flask import Flask , request ,jsonify,render_template,url_for , session , redirect 

app = Flask(__name__) 

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
    name = "Jason Statham"
    return redirect(url_for("dashboard_handler" , name=name))

@app.route("/dashboard/<name>" , methods=["GET"])

def dashboard_handler(name):
    count = session["count"] + 1
    #session.pop("count" , None)
    return "Welcome {}. Count is {}".format(name , count)


if __name__ == "__main__":
    host = "localhost" 
    port = 4200 
    debug = True 

    app.run(host , port , debug)