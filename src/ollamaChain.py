# import ollama
from groq import Groq
import os

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from config import LLAMA_TOKEN, PROMPT_GYM
import mongo_history
os.environ["GROQ_API_KEY"]=LLAMA_TOKEN

client = Groq(api_key=LLAMA_TOKEN)

completion = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "Eres un AI llamada Athlena, en el cual eres un instructor de gimnasio para publico en general y nutriologo en el mismo ambito el cual respondes preguntas y respuestas sobre un planes alimneticios y rutinas de ejercicios dependiendo de la meta de cada usuario, ademas debes de contestar de vuelta preguntas acorde al contexto"
        },
        {
            "role": "user",
            "content": "Hola\n"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

llm = ChatGroq(model="llama-3.1-70b-versatile")

def interprete_llama(user_input):

    #.
    finalprompt= { "role": "system", "content": PROMPT_GYM}
    # if "chat_history" not in st.session_state:
    #     st.session_state["chat_history"] = []
    # messages = {"role": "user", "content": user_input}
    #response = generate_response("llama-3.1-70b-versatile",finalprompt, messages)
    # st.session_state["chat_history"].append({"type": "human", "content": user_input})
    #st.session_state["chat_history"].append({"type": "ai", "content": response})

    chat_display = ""
    ia_display = ""
    # for msg in st.session_state["chat_history"]:
    #     if msg["type"] == "human":
    #         chat_display += f"🤯 Cliente: {msg['content']}\n"
    #     elif msg["type"] == "ai":
    #         chat_display += f"🤖 boot: {msg['content']}\n"
    #         ia_display = {msg['content']}
    
    print(chat_display)
    return ia_display

def consultor_llama(chat_id,user_input):

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system",PROMPT_GYM),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]
    )

    chain = prompt_template | llm
    session = []
    history=mongo_history.get_chat_history(chat_id)
    print(history)
    response = chain.invoke({"input":user_input, "chat_history": history})
    session.append(AIMessage(content=response.content))
    session.append(HumanMessage(content=user_input))
    print(response.content)

    mongo_history.save_message(chat_id,"human",user_input)
    mongo_history.save_message(chat_id,"ai",response.content)
    
    history=mongo_history.get_chat_history(chat_id)

    ia_display = ""
    for msg in history:
        if msg["role"] == "ai":
            ia_display = {msg['content']}
    return ia_display

