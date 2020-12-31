from datetime import datetime


def log(s, end='\n'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {s}", flush=True, end=end)