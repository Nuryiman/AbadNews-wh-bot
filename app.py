import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

from questions import questions_text

load_dotenv()
api_key = os.getenv("GEMINI_API")


# Создаём память для хранения истории беседы
memory = ConversationBufferMemory(return_messages=True)

prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
Ты помощник. Отвечай только по информации ниже. 
Если вопрос не содержится в контексте — скажи: "Извините, у меня нет информации по этому вопросу."

Контекст:
{context}

Вопрос: {user_input}
Ответ:
""",
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    google_api_key=api_key,
    temperature=0.1  # минимизируем креативность
)

# Создаём цепочку с жёстким промптом
qa_chain = LLMChain(
    llm=llm,
    prompt=prompt_template.partial(context=questions_text)
)


app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '')
    print(request)

    # Прогоняем входящее сообщение через цепочку LangChain с памятью
    response_text = qa_chain.run(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
