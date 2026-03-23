from flask import Flask, request, jsonify

app = Flask(__name__)

# 暫存資料（之後可以換資料庫）
traffic_data = []

@app.route("/")
def home():
    return "Traffic API running"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    traffic_data.append(data)
    return jsonify({"status": "ok"})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(traffic_data[-100:])  # 最近100筆

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)