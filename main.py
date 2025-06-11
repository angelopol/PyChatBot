import json
from ui import runUi
from responses.offline import offlineResponse
from responses.online import onlineResponse

data = {}
with open("business.json", "r", encoding="utf-8") as f:
    data = json.load(f)

runUi(
    data.get("businessName", "Chatbot"),
    [offlineResponse, data.get("options", [])],
    [onlineResponse, data]
)