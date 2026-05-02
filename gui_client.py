import tkinter as tk
import socket
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import os
import random
import time

# -------- BASE --------
base_path = os.path.dirname(os.path.abspath(__file__))

# -------- STATE --------
state = {
    "dark": False,
    "light": False,
    "fan": False,
    "connected": False
}

# -------- THEMES --------
LIGHT_THEME = {
    "bg": "#f8edeb",
    "card": "#ffffff",
    "accent": "#ffafcc",
    "text": "#333",
    "sub": "#777"
}

DARK_THEME = {
    "bg": "#1e1e2f",
    "card": "#2b2b3c",
    "accent": "#a2d2ff",
    "text": "#ffffff",
    "sub": "#aaaaaa"
}

def theme():
    return DARK_THEME if state["dark"] else LIGHT_THEME

# -------- NETWORK --------
def send_command(cmd):
    try:
        start = time.time()

        public_key = RSA.import_key(open(os.path.join(base_path, "public.pem")).read())
        rsa_cipher = PKCS1_OAEP.new(public_key)

        aes_key = get_random_bytes(16)
        enc_aes_key = rsa_cipher.encrypt(aes_key)

        aes_cipher = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = aes_cipher.encrypt_and_digest(cmd.encode())

        client = socket.socket()
        client.settimeout(2)
        client.connect(('localhost', 9999))

        client.send(enc_aes_key)
        client.send(aes_cipher.nonce)
        client.send(tag)
        client.send(ciphertext)
        client.close()

        latency = int((time.time() - start) * 1000)

        state["connected"] = True
        connection_label.config(text=f"🟢 CONNECTED ({latency} ms)", fg="#2d6a4f")
        log(f"✔ {cmd} | {latency}ms")

    except:
        state["connected"] = False
        connection_label.config(text="🔴 OFFLINE", fg="red")
        log("✖ Connection failed")

# -------- LOG --------
def log(msg):
    log_box.insert(tk.END, f"{msg}\n")
    log_box.see(tk.END)

# -------- TOGGLES --------
def toggle_light():
    state["light"] = not state["light"]
    send_command("LIGHT ON" if state["light"] else "LIGHT OFF")
    update_switch(light_switch, state["light"])

def toggle_fan():
    state["fan"] = not state["fan"]
    send_command("FAN ON")
    update_switch(fan_switch, state["fan"])

# -------- SWITCH UI --------
def create_switch(parent, text, command):
    frame = tk.Frame(parent, bg=theme()["card"])
    frame.pack(fill="x", pady=8)

    label = tk.Label(frame, text=text, bg=theme()["card"], fg=theme()["text"], font=("Segoe UI", 11))
    label.pack(side="left", padx=10)

    canvas = tk.Canvas(frame, width=50, height=25, bg=theme()["card"], highlightthickness=0)
    canvas.pack(side="right", padx=10)

    oval = canvas.create_oval(2, 2, 23, 23, fill="white")
    bg = canvas.create_rectangle(0, 0, 50, 25, outline="", fill="#ccc")

    def on_click(event):
        command()

    canvas.bind("<Button-1>", on_click)

    return canvas, oval, bg

def update_switch(widget, on):
    canvas, oval, bg = widget
    if on:
        canvas.itemconfig(bg, fill="#80ed99")
        canvas.coords(oval, 27, 2, 48, 23)
    else:
        canvas.itemconfig(bg, fill="#ccc")
        canvas.coords(oval, 2, 2, 23, 23)

# -------- SENSOR --------
def update_sensors():
    temp = random.randint(24, 35)
    humidity = random.randint(40, 80)
    air = random.choice(["Good", "Moderate", "Poor"])

    temp_label.config(text=f"{temp}°C", fg=color_temp(temp))
    humidity_label.config(text=f"{humidity}%", fg="#457b9d")
    air_label.config(text=air, fg=color_air(air))

    root.after(2000, update_sensors)

def color_temp(t):
    return "#e63946" if t > 30 else "#2a9d8f"

def color_air(a):
    return {"Good": "#2a9d8f", "Moderate": "#e9c46a", "Poor": "#e63946"}[a]

# -------- CONNECTION CHECK --------
def check_connection():
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect(("localhost", 9999))
        s.close()
        if not state["connected"]:
            connection_label.config(text="🟢 CONNECTED", fg="#2d6a4f")
    except:
        connection_label.config(text="🔴 OFFLINE", fg="red")

    root.after(3000, check_connection)

# -------- THEME TOGGLE --------
def toggle_theme():
    state["dark"] = not state["dark"]
    apply_theme()

def apply_theme():
    t = theme()
    root.config(bg=t["bg"])
    main.config(bg=t["bg"])
    title.config(bg=t["bg"], fg=t["text"])
    subtitle.config(bg=t["bg"], fg=t["sub"])

# -------- UI --------
root = tk.Tk()
root.title("Smart Home Pro ✨")
root.geometry("430x780")

main = tk.Frame(root)
main.pack(fill="both", expand=True, padx=15, pady=15)

title = tk.Label(main, text="Smart Home", font=("Segoe UI", 20, "bold"))
title.pack()

subtitle = tk.Label(main, text="AI Powered Dashboard", font=("Segoe UI", 10))
subtitle.pack(pady=5)

tk.Button(main, text="🌗 Toggle Theme", command=toggle_theme).pack(pady=10)

# -------- SENSOR CARDS --------
def card(text):
    f = tk.Frame(main)
    f.pack(fill="x", pady=5)
    tk.Label(f, text=text).pack(anchor="w")
    val = tk.Label(f, font=("Segoe UI", 14, "bold"))
    val.pack(anchor="w")
    return val

temp_label = card("Temperature")
humidity_label = card("Humidity")
air_label = card("Air Quality")

# -------- SWITCHES --------
light_switch = create_switch(main, "Light", toggle_light)
fan_switch = create_switch(main, "Fan", toggle_fan)

# -------- STATUS --------
connection_label = tk.Label(main, text="Checking...", font=("Segoe UI", 10))
connection_label.pack(pady=10)

# -------- LOG --------
log_box = tk.Text(main, height=8, bg="#111", fg="#0f0")
log_box.pack(fill="x", pady=10)

# -------- START --------
apply_theme()
update_sensors()
check_connection()

root.mainloop()