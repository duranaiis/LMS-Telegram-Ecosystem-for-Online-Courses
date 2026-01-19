# Relactation Course Bot 

An automated Telegram bot designed to deliver educational video content for nursing mothers.

## Key Features
* **Structured Lessons:** Step-by-step video delivery across 4 stages of relactation.
* **Content Protection:** Strict `protect_content` mode enabled (prevents forwarding, saving, or screen recording).
* **Access Control:** Automatic membership verification for private Telegram channels.
* **Interactive UI:** Dynamic inline keyboards for homework and navigation.

## Tech Stack
* **Language:** Python 3.10+
* **Framework:** [aiogram 3.x](https://github.com/aiogram/aiogram) (Asynchronous)
* **Deployment:** Amvera Cloud / Docker-ready

## Environment Variables
To keep your bot secure, do not hardcode your tokens. Use environment variables instead:
- `BOT_TOKEN`: Your Telegram Bot API Token from @BotFather.
- `CHANNEL_ID`: The ID of your private channel (e.g., -100...).

## Installation
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set your environment variables.
4. Run: `python main.py`.
