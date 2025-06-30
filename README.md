# Meme Generator Telegram Bot

This is a Telegram bot that generates memes based on chat conversations using AI. It leverages the MagicHour meme generator API and Alchemyst AI for meme topic generation.

## Features
- Analyzes chat history to generate relevant, funny meme topics
- Uses MagicHour API to create memes with popular templates
- Sends generated memes directly in the Telegram chat

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/foxy-dev1/Telegram-MemeGenerator-Bot.git
cd Telegram-MemeGenerator-Bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
Create a `.env` file in the project root with the following content:

```
telegram_bot_key=your_telegram_bot_api_key
meme_gen_api=your_magichour_api_key
alcheyst_api_key=your_alchemyst_api_key 
```

#### How to get the API keys:
- **Telegram Bot API Key:**
  1. Talk to [@BotFather](https://t.me/BotFather) on Telegram.
  2. Use `/newbot` to create a new bot and get your API key.
- **MagicHour API Key:**
  1. Sign up at [MagicHour AI](https://magichour.ai/).
  2. Go to your dashboard and find your API key.
- **Alchemyst API Key:**
  1. Register at [Alchemyst AI](https://getalchemyst.ai/).
  2. Go to your account settings or dashboard to generate an API key.

### 4. Run the bot
```bash
python meme.py
```

## Usage
- Start a chat with your bot or add bot to your group on Telegram.
- Send messages the bot will analyze the conversation and generate memes.

