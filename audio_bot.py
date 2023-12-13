import telebot
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr

bot_token = '5623847598:AAGhF-UhlU6NdzPCfYCICgnHb3nfcWLBlz8'
bot = telebot.TeleBot(token=bot_token)

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the translator
translator = Translator()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello! I am your Telegram bot.')

@bot.message_handler(func=lambda msg: msg.text is not None)
def text_to_speech(message):
    text = message.text
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save("text.mp3")
    audio = open('text.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)

@bot.message_handler(func=lambda msg: msg.text is not None)
def translate_text(message):
    text = message.text
    translated = translator.translate(text, dest='en')
    bot.reply_to(message, translated.text)

@bot.message_handler(content_types=['voice'])
def audio_to_text(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    # Convert ogg file to wav
    # Use appropriate library or tool for conversion
    # Then use the wav file for speech recognition
    with sr.AudioFile('voice.wav') as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
            bot.reply_to(message, text)
        except:
            bot.reply_to(message, "Sorry, I could not recognize your voice.")

bot.polling()
