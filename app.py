from flask import Flask, request, jsonify, abort
from housing.logger import logging
from housing.exception import HousingException


# from flask_cors import CORS
import os
import sys

app = Flask(__name__)
# CORS(app)
PORT = os.environ.get("PORT")
print(PORT)


@app.get("/")
def home():
    try:
        logging.info("Greeted")
        raise Exception("custom exception")
    except Exception as e:
        housing = HousingException(e)
        logging.error(housing.error_message)
    return jsonify({"message": "success"}), 200


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
