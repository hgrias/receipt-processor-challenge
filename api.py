from flask import Flask, request, jsonify, make_response
import uuid

app = Flask(__name__)

receipts = {}


@app.route("/receipts/process", methods=["POST"])
def process_receipts():
    if request.method == "POST":
        data = request.get_json()
        receipt_id = str(uuid.uuid4())
        receipts[receipt_id] = data
        return jsonify({"id": receipt_id})
