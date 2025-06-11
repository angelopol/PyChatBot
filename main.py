import json
from ui import runUi

data = {}
with open("business.json", "r", encoding="utf-8") as f:
    data = json.load(f)

runUi(data.get("businessName", "Chatbot"))