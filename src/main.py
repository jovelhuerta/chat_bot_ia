from flask import Flask,request
import telebot
from config import TELEGRAM_TOKEN, GYM_TELEGRAM_TOKEN,URI_BOT
import ollamaChain
import os

port = int(os.environ.get("PORT", 8080))

botGym= telebot.TeleBot(GYM_TELEGRAM_TOKEN)
boot= telebot.TeleBot(TELEGRAM_TOKEN)

# Configuración del servidor Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "El bot está funcionando correctamente en Cloud Run"

# Configuración de webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        print(f"Datos recibidos: {json_str}")

        update = telebot.types.Update.de_json(json_str)
        botGym.process_new_updates([update])
        return 'Ejecutando bot', 200
    else:
        return 'Contenido no permitido', 403

@botGym.message_handler(commands=['start','help'])
def send_welcome(message):
    botGym.reply_to(message, "Hola Hola")

@botGym.message_handler(content_types=['text'])
def all_message(message):
    print(message)
    response= ollamaChain.consultor_llama(message.chat.id,message.text)
    botGym.send_message(message.chat.id,response)

# Inicia el servidor Flask
if __name__ == '__main__':
    # Establecer el webhook localmente (puedes usar herramientas como ngrok para pruebas externas)
    WEBHOOK_URL = URI_BOT
    botGym.remove_webhook()
    botGym.set_webhook(url=WEBHOOK_URL)

    print(f"Webhook configurado en {WEBHOOK_URL}")
    print("Servidor Flask iniciado. Esperando mensajes...")
    app.run(host='0.0.0.0', port=port, debug=True)


def handle_boot():

 #   @boot.message_handler(commands=['start','help'])
    def send_welcome(message):
        boot.reply_to(message, "Hola Hola")

   # @boot.message_handler(content_types=['text'])
    def hi_message(message):
        #Poner IA para convertirlo en lenguaje natural y poner claves para la respuesta y busquedas internas
        response= ollamaChain.interprete_llama(message.text)
        folio = None
        
        check_response=get_text(response)


        if "error" in check_response.lower():
            print("buscando Error")
            folio= get_folio(check_response.split())
            print(folio)
        if "logs" in check_response.lower():
            print("buscando Logs")
            folio= get_folio(check_response.split())
            print(folio)
            #Buscar todos los logs

    #boot.replay_to(message,response)

    def get_text(response_dict):
        response_text = str(response_dict)

        print(response_text)
        return response_text

    def get_folio(split):
        folio_index = split.index("folio") + 1
        folio = split[folio_index].strip(".}'")
        if "->" in folio:
            folio_index = split.index("folio") + 2
            folio = split[folio_index].strip(".}'")
        if(len(folio)<=2):
            folio_index = split.index("folio") + 2
            folio = split[folio_index].strip(".}'")
        return folio

  #  boot.polling()
#