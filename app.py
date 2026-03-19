from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "EAAM4XwaviZAcBQ45TjzrJpWBVYc2gUxmqCeEhuP63GPraV6uwuzw8JJxMs9HXZBHvq571jCtbY4CCT9enGRz1jm8O6GlkolaHoZAkZCUvkhnCfPVNyIEfLbDhfM58XenUZCduZBeUA2ouoyCKlAvVH7h5Nd91OZB9M1RccdjZB4bjJzpcfWiIgCQo8VHsPQrMPLxapVdfzug626wKYujPs8Xndw2DmuadkDj96yLTnrR1URFK99ZC4BZCPSFo29mq8V99JErQYnfrgaVVvkf5KCE5x"
PHONE_ID = "1065145956681916"

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    requests.post(url, headers=headers, json=data)

def calculate(msg):
    try:
        crop, soil, rain = msg.split()

        score = 0
        if soil == "low": score += 3
        if rain == "no": score += 2
        if crop == "paddy": score += 3

        if score >= 6:
            return "🌾 Irrigate Tomorrow (3 hrs)"
        elif score >= 4:
            return "🌾 Irrigate in 2 days"
        else:
            return "🌾 Irrigate in 4 days"
    except:
        return "Send like: paddy low no"

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == "mytoken":
            return request.args.get("hub.challenge")
        return "Error"

    data = request.json

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = msg["text"]["body"]
        sender = msg["from"]

        reply = calculate(text)
        send_message(sender, reply)
    except:
        pass

    return "OK"

app.run(port=5000)
