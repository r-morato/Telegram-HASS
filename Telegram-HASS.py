import os
import requests
from telegram.client import Telegram
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
DATABASE_ENCRYPTION_KEY = os.getenv("DATABASE_ENCRYPTION_KEY")

HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
COFFEE_MACHINE_ENTITY_ID = os.getenv("COFFEE_MACHINE_ENTITY_ID")
CLIMATE_UPSTAIRS = os.getenv("CLIMATE_UPSTAIRS")
CLIMATE_DOWNSTAIRS = os.getenv("CLIMATE_DOWNSTAIRS")
HUMIDIFIER_ENTITY_ID = os.getenv("DEHUMIDIFIER")

# Initialize Telegram client
tg = Telegram(
    api_id=API_ID,
    api_hash=API_HASH,
    phone=PHONE,
    database_encryption_key=DATABASE_ENCRYPTION_KEY
)

tg.login()

def log_command(message_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("home_assistant_commands.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message_text}\n")

def send_switch_command(entity_id, action):
    url = f"{HOME_ASSISTANT_URL}/api/services/switch/turn_{action}"
    headers = {
        'Authorization': f'Bearer {HOME_ASSISTANT_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = { 'entity_id': entity_id }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully turned {action} {entity_id}")
    else:
        print(f"Failed to turn {action} {entity_id}: {response.status_code} {response.text}")

def set_climate_mode_and_temp(entity_id, mode, temperature=None):
    headers = {
        'Authorization': f'Bearer {HOME_ASSISTANT_TOKEN}',
        'Content-Type': 'application/json'
    }

    hvac_url = f"{HOME_ASSISTANT_URL}/api/services/climate/set_hvac_mode"
    hvac_payload = {
        'entity_id': entity_id,
        'hvac_mode': mode
    }
    hvac_response = requests.post(hvac_url, headers=headers, json=hvac_payload)
    if hvac_response.status_code == 200:
        print(f"Set HVAC mode to {mode} for {entity_id}")
    else:
        print(f"Failed to set HVAC mode: {hvac_response.status_code} {hvac_response.text}")

    if temperature is not None:
        temp_url = f"{HOME_ASSISTANT_URL}/api/services/climate/set_temperature"
        temp_payload = {
            'entity_id': entity_id,
            'temperature': temperature
        }
        temp_response = requests.post(temp_url, headers=headers, json=temp_payload)
        if temp_response.status_code == 200:
            print(f"Set temperature to {temperature}°C for {entity_id}")
        else:
            print(f"Failed to set temperature: {temp_response.status_code} {temp_response.text}")

def send_service_command(domain, service, entity_id):
    url = f"{HOME_ASSISTANT_URL}/api/services/{domain}/{service}"
    headers = {
        'Authorization': f'Bearer {HOME_ASSISTANT_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'entity_id': entity_id
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully called {domain}.{service} on {entity_id}")
    else:
        print(f"Failed to call {domain}.{service} on {entity_id}: {response.status_code} {response.text}")

def extract_temperature(text):
    parts = text.split()
    for part in parts:
        try:
            temp = float(part)
            if 15.0 <= temp <= 24.0:
                return temp
        except ValueError:
            continue
    return 19.0

def new_message_handler(update):
    message_content = update['message']['content']
    message_text = message_content.get('text', {}).get('text', '').lower().strip()
    
    print(f"Received message: {message_text}")

    # Coffee
    if "turn on coffee machine" in message_text:
        send_switch_command(COFFEE_MACHINE_ENTITY_ID, "on")
        log_command(message_text)
    elif "turn off coffee machine" in message_text:
        send_switch_command(COFFEE_MACHINE_ENTITY_ID, "off")
        log_command(message_text)

    # Heating
    elif "turn on heating upstairs" in message_text:
        temp = extract_temperature(message_text)
        set_climate_mode_and_temp(CLIMATE_UPSTAIRS, "heat", temp)
        log_command(f"turn on heating upstairs {temp}")
    elif "turn off heating upstairs" in message_text:
        set_climate_mode_and_temp(CLIMATE_UPSTAIRS, "off")
        log_command(message_text)
    elif "turn on heating downstairs" in message_text:
        temp = extract_temperature(message_text)
        set_climate_mode_and_temp(CLIMATE_DOWNSTAIRS, "heat", temp)
        log_command(f"turn on heating downstairs {temp}")
    elif "turn off heating downstairs" in message_text:
        set_climate_mode_and_temp(CLIMATE_DOWNSTAIRS, "off")
        log_command(message_text)

    # Humidifier
    elif "turn on dehumidifier" in message_text:
        send_service_command("humidifier", "turn_on", HUMIDIFIER_ENTITY_ID)
        log_command(message_text)
    elif "turn off dehumidifier" in message_text:
        send_service_command("humidifier", "turn_off", HUMIDIFIER_ENTITY_ID)
        log_command(message_text)

    # Raw Home Assistant service call
    elif message_text.startswith("call service"):
        try:
            _, domain, service, entity_id = message_text.split(" ", 3)
            send_service_command(domain, service, entity_id)
            log_command(message_text)
        except ValueError:
            print("Invalid format. Use: call service <domain> <service> <entity_id>")

# Register the message handler
tg.add_message_handler(new_message_handler)

# Run the bot
tg.idle()
