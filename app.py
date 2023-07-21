from flask import Flask , request ,jsonify,render_template

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

if __name__ == "__main__":
    host = "localhost" 
    port = 4200 
    debug = True 

    app.run(host , port , debug)