
from flask import Flask,jsonify
from flask_cors import CORS 
  
app = Flask(__name__) 
CORS(app)

@app.route("/")
def home():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

if __name__ == "__main__":
    app.run()