import logging 
from telegram import Update
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler,filters,MessageHandler
from uuid import uuid4
import asyncio
from magic_hour import Client
import urllib.request
import time
import ast
import requests
import json
import ast

telegram_bot_key="your_telegram_bot_api_key"
meme_gen_api="your_magichour_api_key"
alcheyst_api_key="your_alchemyst_api_key" 

MEME_TEMPLATES = [
    "Drake Hotline Bling",
    "Galaxy Brain", 
    "Two Buttons",
    "Gru's Plan",
    "Tuxedo Winnie The Pooh",
    "Is This a Pigeon",
    "Panik Kalm Panik",
    "Disappointed Guy",
    "Waiting Skeleton",
    "Bike Fall",
    "Change My Mind",
    "Side Eyeing Chloe",
    "Distracted Boyfriend",
    "Random"
]

# System prompt for the meme generator bot
SYSTEM_PROMPT = """You are a creative meme generator bot. Your job is to analyze chat conversations and 
create relevant, funny memes based on the content.

ONLY RESPOND WITH A SINGLE JSON OBJECT. DO NOT include any explanations, greetings, or additional text. DO NOT say anything like 'Here's your meme' or 'Sure!'. Just output the JSON, nothing else.

**Your Task:**
1. Read the chat history and understand the context, emotions, and situations discussed.
2. Identify relatable, funny, or ironic moments that would make good memes.
3. Choose the most appropriate meme template from the available options.
4. Create a witty, relevant topic/caption that captures the essence of the conversation.


**Guidelines:**
- Keep topics concise but descriptive (under 100 characters).
- Match the template to the situation (e.g., use "Two Buttons" for dilemmas).
- Be clever and relatable.
- Avoid offensive or inappropriate content.
- Focus on programming, tech, or general life situations that resonate with developers.
- Make it funny but not mean-spirited.

**Response Format:**
Respond with a **single JSON object** like this:
{
    "topic": "Your witty meme caption/topic here",
    "template": "Exact template name from the list above"
}

"""





async def get_process_messages(messages,top=10):

    try:
        if len(messages)>=1:
            context = list(messages.items())[:top] if len(messages) >= top else list(messages.items())[:-1]
        else:
            return "not enough messages chat more"
        
        url = "https://platform-dev.getalchemystai.com/api/v1/chat/generate"
            
        headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {alcheyst_api_key}"
            }
            

        data = {
                "chat_history": [
                    {"content":SYSTEM_PROMPT + str(MEME_TEMPLATES),"role":"system"},
                    {"content": context , "role": "user"}
                ],
                "persona": ""
            }
            
        response = requests.post(url, headers=headers, json=data)

        
        if response:
            result = json.loads(response.text)["result"]
            content  = result["response"]["kwargs"]["content"]
            content = response.content
            cleaned = content.replace('```json', '').replace('```', '').strip()
            cleaned = ast.literal_eval(cleaned)
            template = cleaned["template"]
            topic = cleaned["topic"]
            return {"template":template,"topic":topic}
        
        else:
            return f"response not found {response}"
    except Exception as e:
        return f"error while executing error{e}"





async def generate_meme(topic,template):
    url = "https://api.magichour.ai/v1/ai-meme-generator"
    payload = {
        "name": "My Funny Meme",
        "style": {
            "topic": topic,
            "template": template,
            "searchWeb": False
        }
    }
    headers = {
        "Authorization": f"Bearer {meme_gen_api}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response





logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

messages = {}
MAX_TRY = 30
DELAY = 1

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id
                                   ,text="hello iam a meme bot")
    print(update.message.text)

async def unknown(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="unknown command")    
    
async def echo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    
    # chat_type = update.effective_chat.type
    user_name = update.effective_user.first_name
    message_text = update.message.text

    message_id = str(uuid4())
    messages[message_id] = {
        # "chat_type":chat_type,
        "user_name":user_name,
        "message_text":message_text

    }

    print(f"user: {user_name}, text: {message_text}")

async def creatememe(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_response = await get_process_messages(messages)
    client = Client(token=meme_gen_api)

    if isinstance(message_response,dict):
        template = message_response["template"]
        topic = message_response["topic"]
        meme_response = await generate_meme(topic,template)

        if meme_response:
            output_file = "output.png"
            response_id  = ast.literal_eval(meme_response.text)["id"]

            for _ in range(MAX_TRY):
                res = client.v1.image_projects.get(id=response_id)
                if res.status == "complete":
                    print("render complete!")
                    with (
                        urllib.request.urlopen(res.downloads[0].url) as response,
                        open(output_file, "wb") as out_file,
                    ):
                        out_file.write(response.read())
                    print(f"file downloaded successfully to {output_file}")
                    with open(output_file,"rb") as photo_file:
                        await context.bot.send_photo(chat_id=update.effective_chat.id,photo=photo_file)
                    break
                
                elif res.status == "error":
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Render failed.")
                    print("render failed")
                    break
                
                else:
                    await asyncio.sleep(DELAY)


    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=message_response)

            
            

application = ApplicationBuilder().token(telegram_bot_key).build()

start_handler = CommandHandler("start",start)
unknown_handler = MessageHandler(filters.COMMAND,unknown)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),echo)
create_meme_handler = MessageHandler(None,creatememe)

application.add_handlers([start_handler,echo_handler,create_meme_handler,unknown_handler])


application.run_polling()