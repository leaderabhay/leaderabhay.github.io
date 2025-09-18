from flask import Flask, request, jsonify, send_from_directory
import requests
import random
import string
import datetime
import os

app = Flask(__name__)

# Your bot details
BOT_TOKEN = "8302104778:AAFwmnWLqo4FJK3Wz9uvRg-mD_n_kKv_5OA"
CHAT_ID = "7768630615"   # 👈 your Telegram user ID

def generate_order_id():
    return "FFVL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    uid = data.get("uid")
    server = data.get("server")
    telegram = data.get("telegram")
    plan_type = data.get("plan_type")
    plan_duration = data.get("plan_duration")
    price = data.get("price")
    txn_id = data.get("transaction_id")

    order_id = generate_order_id()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
🎉 New Order Received 🎉

Order ID: {order_id}
Plan: {plan_type} ({plan_duration})
Amount: ₹{price}
UID: {uid}
Server: {server}
Telegram: {telegram}
Transaction ID: {txn_id}
Date: {date}
"""

    # Send to Telegram bot
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)

    try:
        result = response.json()
    except Exception:
        result = {"error": "Invalid response from Telegram"}

    return jsonify({"success": response.ok, "telegram_response": result, "order_id": order_id})

if __name__ == "__main__":
    app.run(debug=True)