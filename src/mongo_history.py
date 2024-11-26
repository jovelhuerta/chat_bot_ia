from pymongo import MongoClient
from datetime import datetime
from config import URI


client = MongoClient(URI)
client._timeout=30000,
client.so
db = client.Chat_Gym  # Base de datos llamada 'Chat_Gym'
chat_collection = db.chat_history  # Colección de historial llamada 'chat_history'



def save_message(user_id, role, content):
    message = {
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": datetime.now()  # Timestamp para la fecha y hora del mensaje
    }
    chat_collection.insert_one(message)  # Inserta el mensaje en la colección

# Función para obtener el historial de un usuario específico
def get_chat_history(user_id):
    messages = chat_collection.find({"user_id": user_id}).sort("timestamp", 1)  # Ordena por timestamp
    return list(messages)

# Función para mostrar los mensajes
def display_chat_history(user_id):
    history = get_chat_history(user_id)
    if not history:
        print("No se encontraron mensajes para este usuario.")
    else:
        for message in history:
            timestamp = message["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} - {message['role'].capitalize()}: {message['content']}")