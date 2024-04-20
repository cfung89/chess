from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import game


app = Flask(__name__)
Cors(app)

@app.route('/create', methods=['POST'])
def new_game():
   pass 

if __name__ == "__main__":
    app.run(debug=True)
