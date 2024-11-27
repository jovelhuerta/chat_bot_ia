from flask import Flask,request
import telebot
from config import TELEGRAM_TOKEN, GYM_TELEGRAM_TOKEN,URI_BOT
import ollamaChain
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

botGym= telebot.TeleBot(GYM_TELEGRAM_TOKEN,threaded=False)
botGym.remove_webhook()
botGym.set_webhook(url=URI_BOT)

boot= telebot.TeleBot(TELEGRAM_TOKEN)

# Ruta para el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        print("Solicitud recibida en /webhook")
        json_string = request.get_data().decode('utf-8')
        print(f"Payload recibido: {json_string}")
        update = telebot.types.Update.de_json(json_string)
        #botGym.polling()
        botGym.process_new_updates([update])
        print("Actualización procesada correctamente")
    except Exception as e:
        print(f"Error procesando la actualización: {e}")
    return "OK", 200

# Ruta principal opcional (puedes usarla para verificar que la app esté activa)
@app.route('/')
def index():
    webhook()
    return "El bot está funcionando correctamente en Cloud Run", 200


@botGym.message_handler(commands=['start','help'])
def send_welcome(message):
    print(message)
    botGym.reply_to(message, "Hola Hola")

@botGym.message_handler(content_types=['text'])
def all_message(message):
    print(message)
    response= ollamaChain.consultor_llama(message.chat.id,message.text)

    botGym.send_message(message.chat.id,response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
#
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