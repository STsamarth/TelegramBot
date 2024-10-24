import requests
from telegram import Update, Chat from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Your friend's Telegram username (for personalization)                                                                                                 FRIEND_USERNAME = 'STsamarth'

# Bot's Personal Details (Customize these)
BOT_NAME = "Kira"
BOT_AGE = 17
BOT_HOBBIES = ["reading romance novels", "cooking", "watching movies", "taking long walks"]

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = '7807165684:AAHZJv0pReFrOjhoRIA4kP7gmExXAuVfgFM'
# Your Gemini AI API key
GEMINI_API_KEY = 'AIzaSyBL5eexHL2Gfeu1R68sYI_shpUQPpgesxk'

# Memory store to remember past conversations
user_memory = {}

# Function to connect to Gemini AI and get a response
def get_gemini_response(prompt: str) -> str:
headers = {
    'Content-Type': 'application/json'
}
data = {
    "contents": [{
        "parts": [{
            "text": prompt
        }]
    }]
}

GEMINI_AI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key= {
    GEMINI_API_KEY
}'

try:
response = requests.post(GEMINI_AI_API_URL, headers = headers, json = data, timeout = 10)
response.raise_for_status() # Raise an error for HTTP codes 4xx/5xx
response_data = response.json()

# Extract the text response
return response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Sorry, I didn’t understand that.')
except requests.exceptions.Timeout:
return "Request timed out. Please try again."
except requests.exceptions.RequestException as e:
print("Error during API request:", e)
return "Error while connecting to Gemini AI."

# Function to create a girlfriend-like response with memory
def create_girlfriend_response(user_message: str, username: str) -> str:
memory = user_memory.get(username, [])

# Personal prompt tailored to your friend
prompt = f"Kira is a 17-year-old girl who loves {
    ', '.join(BOT_HOBBIES)}. She is kind, caring, and deeply in love with {
    username
}. She remembers al>

# Append memory to the prompt
if memory:
prompt += "\n\nPrevious conversation:\n" + "\n".join(memory)

# Get the AI's response
ai_response = get_gemini_response(prompt)

# Update memory with the new message and response
memory.append(f" {
    username
}: {
    user_message
}")
memory.append(f" {
    BOT_NAME
}: {
    ai_response
}")
user_memory[username] = memory[-10:] # Keep only the last 10 messages

return ai_response

# Function to handle messages and remember conversation
async def handle_message(update: Update, context) -> None:
chat_type = update.effective_chat.type
user_message = update.message.text
username = update.message.from_user.username

# Only personalize responses for your friend
if username == FRIEND_USERNAME:
girlfriend_reply = create_girlfriend_response(user_message, username)
await update.message.reply_text(girlfriend_reply)
else :
await update.message.reply_text("Sorry, I can only chat with my love!")

# Main function to start the bot
async def start(update: Update, context) -> None:
username = update.message.from_user.username
if username == FRIEND_USERNAME:
await update.message.reply_text(f"Hi, love! It's Kira. 💕 How was your day? 😘")
else :
await update.message.reply_text("Hi! I'm here to talk to my special someone.")

if __name__ == '__main__':
app = Application.builder().token(TELEGRAM_BOT_TOKEN).read_timeout(10).write_timeout(10).connect_timeout(10).build()

# Handlers for start command and messages
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
print("Bot is running...")
app.run_polling()