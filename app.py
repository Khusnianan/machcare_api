from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Config DB dari Railway
db_config = {
    "host": "trolley.proxy.rlwy.net",
    "user": "root",
    "password": "RIgfCDoRMUiRmRGAVvwlgUwAvvlQkPPY",
    "database": "railway",
    "port": 20457
}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "message": "Login success",
            "role": user["role"]
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway kasih port lewat env
    app.run(host="0.0.0.0", port=port)
