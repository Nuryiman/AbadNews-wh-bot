import json
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

from database.crud import get_user_by_phone, create_user, delete_user, update_user_memory
from database.db import AsyncSessionLocal
from database.models import User
from questions import questions_text
from utils import memory_from_json

load_dotenv()
api_key = os.getenv("GEMINI_API")


prompt_template = PromptTemplate(
    input_variables=["context", "history", "user_input"],
    template="""
Ты помощник. Отвечай только по информации ниже. 
Если вопрос не содержится в контексте — скажи: "Извините, у меня нет информации по этому вопросу."
Если пользователь что то не может понять, попробуй объяснить

Контекст:
{context}

История диалога:
{history}


Вопрос: {user_input}
Ответ:

""",
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    google_api_key=api_key,
    temperature=0.2  # минимизируем креативность
)




app = Flask(__name__)
@app.route("/", methods=["POST"])
async def bot():
    incoming_msg = request.values.get('Body', '')
    number = request.values.get('WaId', '')

    async with AsyncSessionLocal() as session:
        user = await get_user_by_phone(session, number)

        if not user:
            user = await create_user(session, number)
            memory = ConversationBufferMemory(return_messages=True)
        elif user.memory:
            memory = memory_from_json(user.memory)
        else:
            memory = ConversationBufferMemory(return_messages=True)

    # Создаём цепочку с жёстким промптом
    qa_chain = LLMChain(
        llm=llm,
        prompt=prompt_template.partial(context=questions_text),
        memory=memory
    )

    # Сначала обрабатываем входящее сообщение
    response_text = qa_chain.run(incoming_msg)
    # Сохраняем только сообщения из памяти
    # Сохранение памяти
    updated_memory_json = json.dumps([msg.dict() for msg in memory.chat_memory.messages])
    await update_user_memory(session=session, phone_number=number, new_memory=updated_memory_json)

    async with AsyncSessionLocal() as session:
        await update_user_memory(session=session, phone_number=number, new_memory=updated_memory_json)

    # Возвращаем ответ
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
