# 🔐 Secure IoT Smart Home System

A full-stack **Smart Home Dashboard** that allows users to securely control IoT devices, monitor real-time sensor data, and track system activity — powered by **RSA + AES encryption** and a modern web interface.

---

## 🌐 Live Features

- 🔐 **User Authentication System**
  - Signup & Login
  - Secure password hashing

- 🔌 **Device Control**
  - Toggle Light, Fan, etc.
  - Device state persistence (per user)

- 📊 **Real-Time Analytics**
  - Live temperature & humidity graphs
  - Dynamic sensor simulation

- 📜 **Activity Logs**
  - User-specific logs
  - Timestamped actions

- 🚨 **Smart Alerts**
  - High temperature warnings
  - Poor air quality alerts

- 🌗 **Dark / Light Mode UI**
  - Clean, modern interface
  - Theme toggle support

- 🔒 **Secure Communication**
  - Hybrid Encryption using **RSA + AES**

---

## 🧠 Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Frontend    | HTML, CSS, JavaScript |
| Backend     | Python (Flask) |
| Encryption  | RSA + AES (PyCryptodome) |
| Database    | JSON (users, logs, devices) |
| Visualization | Chart.js |

---


## 📁 Project Structure
Secure IoT Devices/
│
├── app.py
├── server.py
├── rsa_keys.py
├── users.json
├── logs.json
├── devices.json
├── public.pem
├── private.pem
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── signup.html
│ ├── devices.html
│ ├── analytics.html
│ ├── logs.html
│
├── static/
│ ├── style.css
│ ├── script.js
│ └── bg.jpg


---

## ⚙️ Installation & Setup

1️⃣ Clone the repository
```bash
git clone https://github.com/ankitaaa04/Secure-IoT-Smart-Home-System-.git
cd Secure-IoT-Smart-Home-System-

2️⃣ Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate

3️⃣ Install dependencies
```bash
pip install -r requirements.txt

4️⃣ Run the application
```bash
python app.py

5️⃣ Open in browser
```bash
http://127.0.0.1:5000

🔐 Security Implementation
RSA used for secure key exchange
AES used for fast symmetric encryption
Hybrid encryption ensures confidential & secure communication

🎯 Key Highlights:
 🧠 Modular backend architecture
 📡 Real-time data simulation
 👤 Multi-user support
 🔄 Dynamic UI updates
 🔐 Security-focused design

🚀 Future Enhancements:
 🌐 Cloud deployment (Render / Railway)
 🗄️ MongoDB integration
 🔄 WebSockets for real-time updates
 📱 Mobile responsive UI
 🤖 AI-based automation

💬 Author
Ankita Rangra

⭐ If you like this project
Give it a ⭐ on GitHub!


