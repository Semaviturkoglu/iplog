from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    log_line = f"{datetime.now()} | IP: {ip} | Agent: {user_agent}\n"
    with open("ip_logs.txt", "a") as f:
        f.write(log_line)
    return "<h1>Hoş geldin!</h1><p>IP adresiniz kaydedildi.</p>"

if __name__ == "__main__":
    app.run()
