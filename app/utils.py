import requests
import tempfile
import mimetypes
import logging

from config import Config
def download_audio(media_id):
    """
        When we receive an audio (ID) from the WhatsApp via the webhook, we need to download the audio to be able to manipulate the audio
        How to manipulate media in WhatsApp: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#retrieve-media-url
    """

    response = requests.get(f"https://graph.facebook.com/{Config.WHATSAPP_GRAPH_VERSION}/{media_id}",headers={"Authorization":f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"})
    response.raise_for_status()
    data = response.json()
    """
        {
            "messaging_product": "whatsapp",
            "url": "<URL>", # valid for 5 minutes only 
            "mime_type": "<MIME_TYPE>",
            "sha256": "<HASH>",
            "file_size": "<FILE_SIZE>",
            "id": "<MEDIA_ID>"
        }
    """

    # Download the file from url and store temp
    logging.info("Received Media Data: ")
    logging.info(data)
    with tempfile.NamedTemporaryFile(delete=False,suffix=mimetypes.guess_extension(data['mime_type'])) as temp_file:
        file_response  = requests.get(data['url'], headers={"Authorization":f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"})

        if file_response.status_code == 200:
            temp_file.write(file_response.content)
            return temp_file
        else:
            raise Exception("Download failed.")


def send_message(phone_number, message):
    """
        Send a simple WhatsApp message to Phone Number
    """

    response = requests.post(f"https://graph.facebook.com/{Config.WHATSAPP_GRAPH_VERSION}/{Config.WHATSAPP_PHONENUMBER_ID}/messages",headers=
                {
                    "Authorization":f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
                    "Content-Type":"application/json"
                },json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": phone_number,
                    "type": "text",
                    "reaction": {
                        "preview_url": False,
                        "body": message
                    }
                })
    response.raise_for_status()



def react_to_message(phone_number,message_id,emoji="\uD83D\uDE00"):
    """
        Just send a simple reaction to a message sent by the counterpart :).
    """
    response = requests.post(f"https://graph.facebook.com/{Config.WHATSAPP_GRAPH_VERSION}/{Config.WHATSAPP_PHONENUMBER_ID}/messages",headers=
                   {
                      "Authorization":f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
                      "Content-Type":"application/json"
                   },json={
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": phone_number,
                        "type": "reaction",
                        "reaction": {
                            "message_id": message_id,
                            "emoji": emoji
                        }
                   })
    response.raise_for_status()
