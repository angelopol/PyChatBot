from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API")
if not api_key:
    print("GEMINI_API environment variable is not set.")
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Error initializing Gemini client: {e}")

def onlineResponse(user_message, data):
    if not client:
        return "El bot no se ha inicializado correctamente, revisa tu conexión."
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="You are a helpful assistant. Answer the user's question based on the provided business data.\n\n"
            f"Business Name: {data.get('businessName', 'Unknown')}\n"
            f"Business Description: {data.get('businessDescription', 'No description available')}\n"
            f"Business Location: {data.get('businessLocation', 'No location available')}\n"
            f"Business Phone: {data.get('businessPhone', 'No phone available')}\n"
            f"Business Email: {data.get('businessEmail', 'No email available')}\n"
            f"Business Website: {data.get('businessWebsite', 'No website available')}\n\n"
            "You have an examples of questions and answers in a json format:\n"
            f"{data.get('options', 'No examples available')}\n\n"
            f"User Message: {user_message}\n\n"
            "Please provide a concise and relevant response based on the business data. And response in the language of the user message.\n",
        )
    except:
        return "El bot no se ha inicializado correctamente, revisa tu conexión."
    return response.text

if __name__ == '__main__':
    import json
    with open("business.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    user_message = input("Escribe tu mensaje: ")
    response = onlineResponse(user_message, data)
    print(f"Bot: {response}")