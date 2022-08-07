from flask import Flask, request, jsonify, abort
from housing.logger import logging
from housing.exception import HousingException

# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


@app.get("/")
def home():
    logging.info("Greeted")
    return jsonify({"message": "success"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
