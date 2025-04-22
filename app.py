
from flask import Flask 
from flask_cors import CORS 
  
app = Flask(__name__) 
CORS(app)

@app.route("/")
@cross_origin() # allow all domains to make requests
def home():
    return "Hello from Flask!"

if __name__ == "__main__":
    app.run()