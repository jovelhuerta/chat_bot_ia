import telebot
from config import TELEGRAM_TOKEN, GYM_TELEGRAM_TOKEN
import ollamaChain

botGym= telebot.TeleBot(GYM_TELEGRAM_TOKEN)

boot= telebot.TeleBot(TELEGRAM_TOKEN)


@botGym.message_handler(commands=['start','help'])
def send_welcome(message):
    print(message)
    botGym.reply_to(message, "Hola Hola")

@botGym.message_handler(content_types=['text'])
def all_message(message):
    print(message)
    response= ollamaChain.consultor_llama(message.chat.id,message.text)

    botGym.send_message(message.chat.id,response)

botGym.polling()
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