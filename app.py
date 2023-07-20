from flask import Flask , request 

app = Flask(__name__) 

@app.route("/" , methods=["GET"])
def index_handler():
    return "Welcome to Flask Lesson" 


#We want to leverage python's list and dictionary for adding, updating, deleting, and get 

users = [] 

@app.route("/users" , methods=["GET" , "POST"]) 
def users_handler():
    if request.method == "GET":
        return "This is the GET Handler"
    
    elif request.method == "POST":
        return "We are yet to implement it"
    

if __name__ == "__main__":
    host = "localhost" 
    port = 4200 
    debug = True 

    app.run(host , port , debug)