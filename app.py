# ===== NEW FILES =====
DEVICES_FILE = "devices.json"
LOG_FILE = "logs.json"
USERS_FILE = "users.json"

import datetime
import random
import os, json
from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ===== HELPERS =====
def read_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except:
                return default
    return default

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ===== USERS =====
def load_users():
    return read_json(USERS_FILE, {})

def save_users(users):
    write_json(USERS_FILE, users)

# ===== LOGS (per user) =====
def add_log(user, action):
    logs = read_json(LOG_FILE, [])
    logs.append({
        "user": user,
        "action": action,
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    })
    write_json(LOG_FILE, logs)

# ===== DEVICES (per user) =====
def load_devices():
    return read_json(DEVICES_FILE, {})

def save_devices(devices):
    write_json(DEVICES_FILE, devices)

def get_user_devices(user):
    devices = load_devices()
    if user not in devices:
        devices[user] = {"light": False, "fan": False}
        save_devices(devices)
    return devices[user]

def update_device(user, name, state):
    devices = load_devices()
    if user not in devices:
        devices[user] = {}
    devices[user][name] = state
    save_devices(devices)

# ===== AUTH =====
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = generate_password_hash(request.form["password"])
        users = load_users()
        if u in users:
            return "User exists ❌"
        users[u] = p
        save_users(users)
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        users = load_users()
        if u in users and check_password_hash(users[u], p):
            session["user"] = u
            return redirect("/")
        return "Invalid ❌"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== PAGES =====
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", user=session["user"])

@app.route("/devices")
def devices():
    if "user" not in session:
        return redirect("/login")
    return render_template("devices.html")

@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")
    return render_template("analytics.html")

@app.route("/logs")
def logs():
    if "user" not in session:
        return redirect("/login")
    return render_template("logs.html")

# ===== DEVICE CONTROL =====
@app.route("/toggle_device", methods=["POST"])
def toggle_device():
    user = session.get("user")
    data = request.json
    name = data["device"]
    state = data["state"]

    update_device(user, name, state)
    add_log(user, f"{name.upper()} → {'ON' if state else 'OFF'}")

    return jsonify({"status": "ok"})

@app.route("/get_devices")
def get_devices():
    user = session.get("user")
    return jsonify(get_user_devices(user))

# ===== LOGS =====
@app.route("/get_logs")
def get_logs():
    user = session.get("user")
    logs = read_json(LOG_FILE, [])
    user_logs = [l for l in logs if l["user"] == user]
    return jsonify(user_logs)

# ===== SENSOR DATA + ALERTS =====
@app.route("/get_data")
def get_data():
    temp = random.randint(25, 40)
    humidity = random.randint(40, 80)
    air = random.choice(["Good","Moderate","Poor"])

    alert = None
    if temp > 35:
        alert = "⚠️ High Temperature!"
    elif air == "Poor":
        alert = "🚨 Air Quality Poor!"

    return jsonify({
        "temp": temp,
        "humidity": humidity,
        "air": air,
        "alert": alert
    })

# ===== RUN =====
if __name__ == "__main__":
    app.run(debug=True)