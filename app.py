
from flask import Flask,jsonify
from flask_cors import CORS 
  
app = Flask(__name__) 
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask!"}),200

@app.route("/api/getPreferences", methods=["GET"])
def get_preferences():
    # preferences = {
    #     "theme": "dark",
    #     "notifications": True,
    #     "language": "en"
    # }
    
    return jsonify({"data":{"preferences":{}}}), 200

if __name__ == "__main__":
    app.run()
    