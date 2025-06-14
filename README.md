
# 🏠 Home Assistant Telegram Bot with Apple Shortcuts Integration

This project lets you control your smart home devices through **Telegram messages**, which can be triggered manually or automatically using **Apple Shortcuts**.

It’s a lightweight bot that connects your Telegram account with Home Assistant using its REST API. Use simple text commands to control devices like:

- ☕️ Coffee Machine  
- 🔥 Heating (Upstairs & Downstairs)  
- 💧 Dehumidifier  
- 🛠 Any Home Assistant service (via advanced "call service" command)

# Why is this necessary?

I tried to achieve this before by just using two bots, one that would listen on my server and another one that would send the message from my phone. However, Telegram does not allow bot-to-bot communication so the messages from one bot are invisible to the other bots. However, using the telegram listernet on the server allows you to get any type of message even if it comes from a bot. 



## ✨ Features

- **Telegram Bot Integration**: Securely control your smart home via Telegram messages.
- **Apple Shortcuts Ready**: Trigger commands from your iPhone using buttons or Siri.
- **Temperature Customization**: Set specific temperatures (15°C–24°C), defaults to 19°C if out of range or missing.
- **Command Logging**: Every valid command is logged with a timestamp.
- **Extensible**: Easily expand to control any Home Assistant service via `"call service"`.

---

## 📦 Requirements

- A [Telegram API application](https://my.telegram.org)
- A running [Home Assistant](https://www.home-assistant.io/) instance with:
  - HTTP access on your local network
  - Long-Lived Access Token
- Python 3.8+
- Apple Shortcuts (optional, for iOS automation)

---

## ⚙️ Setup

1. **Clone this repo:**

   ```bash
   git clone https://github.com/yourusername/home-assistant-telegram-bot.git
   cd home-assistant-telegram-bot
   ```

2. **Create a `.env` file:**

   Copy the example below and fill in your values:

   ```env
   # Telegram API credentials
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   PHONE='+1234567890'
   DATABASE_ENCRYPTION_KEY=your_secure_encryption_key

   # Home Assistant
   HOME_ASSISTANT_URL=http://192.168.X.X:8123
   HOME_ASSISTANT_TOKEN=your_long_lived_token
   COFFEE_MACHINE_ENTITY_ID=switch.coffee_machine_socket
   CLIMATE_UPSTAIRS=climate.upstairs
   CLIMATE_DOWNSTAIRS=climate.downstairs
   DEHUMIDIFIER=humidifier.pro_breeze_20l_compressor_dehumidifier
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the bot:**

   ```bash
   python TeleHASS.py
   ```

---

## 🗣 Supported Telegram Commands

| Command                              | Description                                |
|--------------------------------------|--------------------------------------------|
| `turn on coffee machine`             | Turns on the coffee machine                |
| `turn off coffee machine`            | Turns off the coffee machine               |
| `turn on heating upstairs 21.5`      | Turns on upstairs heating to 21.5°C        |
| `turn off heating upstairs`          | Turns off upstairs heating                 |
| `turn on heating downstairs 20`      | Turns on downstairs heating to 20°C        |
| `turn off heating downstairs`        | Turns off downstairs heating               |
| `turn on dehumidifier`              | Turns on the dehumidifier                  |
| `turn off dehumidifier`             | Turns off the dehumidifier                 |
| `call service <domain> <service> <entity_id>` | Executes a raw Home Assistant service |

⚠️ If no valid temperature is provided for heating (or it’s out of range), the system defaults to **19.0°C**.

---

## 🍎 Apple Shortcuts Integration (Optional)

You can integrate this system with **Apple Shortcuts** for quick access:

1. Create shortcut
2. Input the command text and assign it to a variable
3. Input the Conversation ID and assign it to a variable
4. Input Telegram Bot token and assign it to a variable
5. Input the API endpoint and embed the bot token into it
6. Add the post request task and include the conversation ID and command into the parameters
<img width="412" alt="Screenshot 2025-06-14 at 19 09 54" src="https://github.com/user-attachments/assets/109f0da3-b08c-483a-97e5-69c83c1c4d77" /><img width="410" alt="Screenshot 2025-06-14 at 19 14 30" src="https://github.com/user-attachments/assets/6b529ca6-1c06-4d63-9602-6d8d17287c06" /><img width="411" alt="Screenshot 2025-06-14 at 19 17 50" src="https://github.com/user-attachments/assets/8f8f2010-9e60-4306-94ce-b3c45de4d44d" />



---

## 📁 Logging

All executed control commands are logged to `home_assistant_commands.log` with timestamps.

---

## 🤖 Built With

- [python-telegram](https://github.com/eternnoir/pyTelegramBotAPI)
- [requests](https://docs.python-requests.org/en/latest/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

---

## 💡 Future Ideas

- Support for lights, blinds, and scenes
- Web dashboard for logs and live control

---

## 📜 License

MIT License. Feel free to use, fork, and enhance!

Any suggestions or issues please feel free to reach out

---
