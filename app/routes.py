from flask import Blueprint,jsonify, request
from config import Config
import logging
from .utils import download_audio, react_to_message, send_message, get_processed_messages, log_processed_message
import whisper

main = Blueprint('main',__name__)
processed_messages =[] #avoid replay

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)



@main.route("/api/v1/ping",methods = ['GET'])
def ping():
    return jsonify({'message':'pong.'})



@main.route("/api/v1/receive-message",methods=['POST','GET'])
def receive_message():
    """
        To be able to receive messages from WhatsApp (the voice note for now), we need to set up the webhook that will be called when a message is received.
        Getting started with WhatsApp Cloud API: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
        Creating a webhook: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks
        To expose your server and test from your local device, you can use tools like Ngrok (https://ngrok.com/) and do `ngrok http ${port}`
    """
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
        data  = request.get_json()
        logging.info(data) # the payload sent from WhatsApp
        if "messages" not in data["entry"][0]["changes"][0]["value"]:
            logging.info("No Message object in data:")
            logging.info(data["entry"][0]["changes"][0]["value"])
            return "ok", 200
        
        messages = data["entry"][0]["changes"][0]["value"]["messages"]
        user_phone_number =  messages[0]["from"]
        message_id = messages[0]["id"]
            
    
                
        if "audio" in messages[0] and "id" in messages[0]["audio"]:

            audio_id = messages[0]["audio"]["id"]
            logging.info(f"Sender Phone Number: {user_phone_number}, Message ID: {message_id}")
            logging.info("Audio ID: {}".format(audio_id))
            
            if message_id in processed_messages:
                logging.info(f"{message_id} already processed. Exiting...") 
                return "Ok", 200
            # let me react to the message :)
            react_to_message(phone_number=user_phone_number, message_id=message_id, emoji= "\u23F3" ) #⏳

            # Download the audio file.
            audio_file = download_audio(audio_id)  

            react_to_message(phone_number=user_phone_number, message_id=message_id, emoji= "\uD83D\uDC42" ) #👂

            # process the audio
            model = whisper.load_model("turbo")

            logging.info(f"the audio file {audio_file.name}")

            result = model.transcribe(audio_file.name)

            if message_id in processed_messages:
                logging.info(f"{message_id} already processed. Exiting...") 
                return "Ok", 200
            processed_messages.append(message_id)

            react_to_message(phone_number=user_phone_number, message_id=message_id, emoji= "\uD83D\uDC4C" ) #👌
            
            logging.info(f"the response {result}")
            # send reply
            
            send_message(user_phone_number,result["text"])

            
            
            return "ok", 200
        else:
            logging.info(" Could not extract data")
            return "ok", 200
        
        