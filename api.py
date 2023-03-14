from flask import Flask, request, jsonify
from flask_expects_json import expects_json
from datetime import datetime
from math import ceil
import uuid
import os

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
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "shortDescription": {"type": "string"},
                    "price": {"type": "string"},
                },
                "required": ["shortDescription", "price"],
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
def process_receipt():
    if request.method == "POST":
        data = request.get_json()
        receipt_id = str(uuid.uuid4())
        try:
            data["points"] = calculate_points(data)
        except ValueError as e:
            return {
                "ERROR": "Value Error",
                "MESSAGE": str(e),
            }, 400
        receipts[receipt_id] = data
        return {"id": receipt_id}, 200


@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_receipt_points(receipt_id):
    try:
        return {"points": receipts[receipt_id]["points"]}, 200
    except KeyError as e:
        return {
            "ERROR": "Receipt Not Found",
            "MESSAGE": f"Receipt ID {e.args[0]} does not exist.",
        }, 404


def calculate_points(receipt_json):
    # Keep track of total points
    points_total = 0

    # 1 point for each alphanumeric char in the retailer name
    for char in receipt_json["retailer"]:
        if char.isalnum():
            points_total += 1

    # 50 points if total is round dollar amount
    if float(receipt_json["total"]).is_integer():
        points_total += 50

    # 25 points if total is a multiple of 0.25
    if float(receipt_json["total"]) % 0.25 == 0:
        points_total += 25

    # 5 points for every 2 items on the receipt
    points_total += (len(receipt_json["items"]) // 2) * 5

    # Trimmed length of item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    # Then add that to the points.
    for item in receipt_json["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points_total += ceil(float(item["price"]) * 0.2)

    # 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt_json["purchaseDate"], "%Y-%m-%d")
    if int(purchase_date.day) % 2 != 0:
        points_total += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    start_time = datetime.strptime("14:00", "%H:%M")
    end_time = datetime.strptime("16:00", "%H:%M")
    purchase_time = datetime.strptime(receipt_json["purchaseTime"], "%H:%M")
    if start_time <= purchase_time < end_time:
        points_total += 10

    return points_total


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
