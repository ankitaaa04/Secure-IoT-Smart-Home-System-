import socket
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA

# Load private key
private_key = RSA.import_key(open("private.pem").read())
rsa_cipher = PKCS1_OAEP.new(private_key)

# Server setup
server = socket.socket()
server.bind(('localhost', 9999))
server.listen(1)

print("🚀 Server is running... Waiting for connection...")

while True:
    conn, addr = server.accept()
    print(f"🔗 Connected to {addr}")

    try:
        # Receive encrypted AES key
        enc_aes_key = conn.recv(256)
        aes_key = rsa_cipher.decrypt(enc_aes_key)

        # Receive encrypted data
        nonce = conn.recv(16)
        tag = conn.recv(16)
        ciphertext = conn.recv(1024)

        aes_cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        command = aes_cipher.decrypt_and_verify(ciphertext, tag).decode()

        print("📩 Command received:", command)

        # Simulated IoT actions
        if command == "LIGHT ON":
            print("💡 Light turned ON")
        elif command == "LIGHT OFF":
            print("💡 Light turned OFF")
        elif command == "FAN ON":
            print("🌀 Fan turned ON")
        else:
            print("❓ Unknown command")

    except Exception as e:
        print("⚠️ Error:", e)

    conn.close()
    
    