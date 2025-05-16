from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "привет" in incoming_msg:
        msg.body("Привет! Чем могу помочь?")
    elif "помощь" in incoming_msg:
        msg.body("Доступные команды: привет, помощь")
    else:
        msg.body("Извините, я не понимаю эту команду.")

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(debug=True)
