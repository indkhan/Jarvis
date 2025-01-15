import json

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "email": {
                "address": "",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587
            },
            "apps": {},
            "voice_settings": {
                "rate": 150,
                "volume": 1.0
            },
            "news_sources": []
        }