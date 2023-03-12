from flask import Flask, request, jsonify
from flask_expects_json import expects_json
from datetime import datetime
from math import ceil
import uuid

app = Flask(__name__)


schema = {
    "type": "object",
    "properties": {
        "retailer": {"type": "string"},
        "purchaseDate": {"type": "string"},
        "purchaseTime": {"type": "string"},
        "total": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "shortDescription": {"type": "string"},
                "price": {"type": "string"},
            },
        },
    },
    "required": ["retailer", "purchaseDate", "purchaseTime", "total", "items"],
}

receipts = {}


@app.route("/receipts/list", methods=["GET"])
def get_receipts():
    return jsonify(receipts)


@app.route("/receipts/process", methods=["POST"])
@expects_json(schema)
def process_receipts():
    if request.method == "POST":
        data = request.get_json()
        receipt_id = str(uuid.uuid4())
        receipts[receipt_id] = data
        return jsonify({"id": receipt_id})


@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def calculate_points(receipt_id):
    # Get the receipt data
    data = receipts[receipt_id]

    # Keep track of total points
    points_total = 0

    # 1 point for each alphanumeric char in the retailer name
    for char in data["retailer"]:
        if char.isalnum():
            points_total += 1

    # 50 points if total is round dollar amount
    if float(data["total"]).is_integer():
        points_total += 50

    # 25 points if total is a multiple of 0.25
    if float(data["total"]) % 0.25 == 0:
        points_total += 25

    # 5 points for every 2 items on the receipt
    points_total += (len(data["items"]) // 2) * 5

    # Trimmed length of item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    # Then add that to the points.
    for item in data["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points_total += ceil(float(item["price"]) * 0.2)

    # 6 points if the day in the purchase date is odd
    if int(data["purchaseDate"].split("-")[2]) % 2 != 0:
        points_total += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    start_time = datetime.strptime("14:00", "%H:%M")
    end_time = datetime.strptime("16:00", "%H:%M")
    purchase_time = datetime.strptime(data["purchaseTime"], "%H:%M")
    if start_time <= purchase_time < end_time:
        points_total += 10

    return jsonify({"points": points_total})
