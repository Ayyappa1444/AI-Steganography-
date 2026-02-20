import datetime

def log_action(user, action):
    with open("logs/audit.log", "a") as f:
        f.write(f"{datetime.datetime.now()} | {user} | {action}\n")
