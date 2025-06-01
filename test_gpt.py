from app import api_key
from google import genai
client = genai.Client(api_key=api_key)

for item in range(1000):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="привет",
    )
    print(item)
    print(response.text)
    print("----------------")

"""
"{\"chat_memory\":{\"messages\":[{\"content\":\"\u0414\u0430\u0432\u0430\u0439 \u043f\u043e\u0441\u0447\u0438\u0442\u0430\u0435\u043c \u043e\u0442 0 \u0434\u043e 10 \u043f\u043e \u043e\u0447\u0435\u0440\u0435\u0434\u0438\",\"additional_kwargs\":{},\"response_metadata\":{},\"type\":\"human\",\"name\":null,\"id\":null},{\"content\":\"\u0425\u043e\u0440\u043e\u0448\u043e, \u0434\u0430\u0432\u0430\u0439! \u042f \u043d\u0430\u0447\u043d\u0443:\\n\\n**0**\\n\\n\u0422\u0432\u043e\u044f \u043e\u0447\u0435\u0440\u0435\u0434\u044c.\",\"additional_kwargs\":{},\"response_metadata\":{},\"type\":\"ai\",\"name\":null,\"id\":null}]},\"output_key\":null,\"input_key\":null,\"return_messages\":true,\"human_prefix\":\"Human\",\"ai_prefix\":\"AI\",\"memory_key\":\"history\"}"
"""