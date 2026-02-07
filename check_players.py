import socket
import json
import os
import urllib.request
from datetime import datetime

SERVER_IP = "79.127.167.234"
SERVER_PORT = 11317  # change if needed
STATE_FILE = "state.json"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

def get_player_count():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((SERVER_IP, SERVER_PORT))
    s.sendall(b"\x01")
    data = s.recv(1024)
    s.close()

    if not data:
        return 0

    return data[0]

def load_last_count():
    if not os.path.exists(STATE_FILE):
        return 0
    with open(STATE_FILE, "r") as f:
        return json.load(f).get("count", 0)

def save_last_count(count):
    with open(STATE_FILE, "w") as f:
        json.dump({"count": count}, f)

def notify():
    payload = json.dumps({
        "content": f"A player joined at {datetime.utcnow()} UTC"
    }).encode("utf-8")

    req = urllib.request.Request(
        WEBHOOK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "terraria-monitor"
        }
    )
    urllib.request.urlopen(req)

def main():
    current = get_player_count()
    last = load_last_count()

    if last == 0 and current > 0:
        notify()

    save_last_count(current)

main()


