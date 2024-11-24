from flask import Blueprint,jsonify, request
from config import Config
import logging

main = Blueprint('main',__name__)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)



@main.route("/api/v1/ping",methods = ['GET'])
def ping():
    return jsonify({'message':'pong.'})


"""
To be able to receive messages from WhatsApp (the voice note for now), we need to set up the webhook that will be called when a message is received.
Getting started with WhatsApp Cloud API: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
Creating a webhook: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks
To expose your server and test from your local device, you can use tools like Ngrok (https://ngrok.com/) and do `ngrok http ${port}`
"""

@main.route("/api/v1/receive-message",methods=['POST','GET'])
def receive_message():
    # WhatsApp incorporates a system to verify the webhook by sending different parameters
    # More information: https://developers.facebook.com/docs/graph-api/webhooks/getting-started#create-endpoint
    # The verification comes with a hub.mode, hub.challenge and hub.verify_token parameter. The verify_token is 
    # the parameter you set in the developer console and you must return the same hub.challenge value. The verification
    # is done via GET while the actual data is sent via POST

    if request.method == "GET":
        hubmode =  request.args.get("hub.mode")
        hubchallenge =  request.args.get("hub.challenge")
        hubverifytoken = request.args.get("hub.verify_token")


        if hubverifytoken != Config.WHATSAPP_WEBHOOK_TOKEN:
            logging.error(" The token received is not the same set by the user ")
            return "Forbidden", 403
        else:
            logging.info(" Token is same.")
            return hubchallenge, 200

    elif request.method == "POST":
        content  = request.get_json()
        print(content)