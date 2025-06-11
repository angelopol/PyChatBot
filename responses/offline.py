import random

def offlineResponse(user_message, options):
    if not options:
        return "No hay opciones disponibles para responder. Por favor, verifica la configuración del bot."
    user_message_lower = user_message.lower()
    last_response = None
    for option in options:
        for keyword in option["keywords"]:
            if keyword.lower() in user_message_lower:
                if option["responses"]:
                    last_response = random.choice(option["responses"])
    if last_response:
        return last_response
    return "¡Lo siento! No entendí tu pregunta. ¿Puedes reformularla?"

if __name__ == "__main__":
    import json
    with open("business.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    options = data.get("options", [])
    user_message = input("Escribe tu mensaje: ")
    response = offlineResponse(user_message, options)
    print(f"Bot: {response}")