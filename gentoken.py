import secrets

# Generate a secure random token, for the WhatsApp webhook
token = secrets.token_urlsafe(32)
print(f"Your Webhook Token: {token}")
