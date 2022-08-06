from flask import Flask, request, jsonify

# from flask_cors import CORS
import os

app = Flask(__name__)
# CORS(app)
PORT = os.environ.get("PORT")
print(PORT)


@app.get("/")
def home():
    return jsonify({"message": "success"}), 200


if __name__ == "__main__":
    app.run(port=PORT)
