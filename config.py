import os
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONENUMBER_ID = os.getenv("WHATSAPP_PHONENUMBER_ID")
    WHATSAPP_BUSINESS_ID = os.getenv("WHATSAPP_BUSINESS_ID")
    WHATSAPP_GRAPH_VERSION = os.getenv("WHATSAPP_GRAPH_VERSION","v20.0")
    WHATSAPP_WEBHOOK_TOKEN = os.getenv("WHATSAPP_WEBHOOK_TOKEN")