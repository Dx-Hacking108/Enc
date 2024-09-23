import os
from cryptography.fernet import Fernet
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Generate a random encryption key
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Save the encryption key to a file (optional)
with open('encryption_key.txt', 'wb') as key_file:
    key_file.write(encryption_key)

# Load the encryption key from a file (optional)
# with open('encryption_key.txt', 'rb') as key_file:
#     encryption_key = key_file.read()
# cipher_suite = Fernet(encryption_key)

def encrypt_message(message):
    return cipher_suite.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message.encode()).decode()

def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, this is an encrypted Telegram bot.")

def echo(update: Update, context):
    encrypted_message = encrypt_message(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Encrypted message: {encrypted_message}")

    decrypted_message = decrypt_message(encrypted_message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Decrypted message: {decrypted_message}")

def main():
    updater = Updater(token='6223370595:AAHetPeO0RN3OTU28RRaIyoTyQhZWgFP0SA', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
