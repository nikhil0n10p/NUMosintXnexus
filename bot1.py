import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import geocoder, carrier
import re
import logging
import webbrowser

# Setup logger
logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Escape Markdown (if used in future with Telegram bot)
def escape_markdown(text):
    return re.sub(r"([_*()~`>#+\-=|{}.!])", r"\\\1", text)

# Get basic phone info
def get_phone_info(phone_number):
    try:
        parsed = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(parsed):
            return None, "❌ Invalid Number.\nError: Invalid format or missing region code."

        return {
            "Formatted": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "Location": geocoder.description_for_number(parsed, "en"),
            "Carrier": carrier.name_for_number(parsed, "en")
        }, None
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return None, f"❌ Invalid Number.\nError: {str(e)}"

# Trace deeper info from CallTracer
def trace_calltracer_info(phone_number):
    url = "https://calltracer.in"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"country": "IN", "q": phone_number}

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        details = {
            "Complaints": soup.find(string="Complaints").find_next("td").text,
            "Owner Name": soup.find(string="Owner Name").find_next("td").text,
            "Mobile State": soup.find(string="Mobile State").find_next("td").text,
            "IMEI number": soup.find(string="IMEI number").find_next("td").text,
            "MAC address": soup.find(string="MAC address").find_next("td").text,
            "Connection": soup.find(string="Connection").find_next("td").text,
            "IP address": soup.find(string="IP address").find_next("td").text,
            "Owner Address": soup.find(string="Owner Address").find_next("td").text,
            "Hometown": soup.find(string="Hometown").find_next("td").text,
            "Reference City": soup.find(string="Refrence City").find_next("td").text,
            "Owner Personality": soup.find(string="Owner Personality").find_next("td").text,
            "Language": soup.find(string="Language").find_next("td").text,
            "Mobile Locations": soup.find(string="Mobile Locations").find_next("td").text,
            "Country": soup.find(string="Country").find_next("td").text,
            "Tracking History": soup.find(string="Tracking History").find_next("td").text,
            "Tracker Id": soup.find(string="Tracker Id").find_next("td").text,
            "Tower Locations": soup.find(string="Tower Locations").find_next("td").text,
        }
        return details
    except Exception:
        return None

# Main function
def main():
    telegram_channel_url = "https://t.me/addlist/uOO_2SYnwyI4MjE1"
    print("🔍 Welcome to the OSINT Detective Tool!")
    print(f"📢 Join our Telegram for updates: {telegram_channel_url}\n")

    webbrowser.open(telegram_channel_url)

    while True:
        phone_number = input("📲 Enter a phone number (or 'exit'): ").strip()
        if phone_number.lower() == "exit":
            print("👋 Goodbye!")
            break

        print("\n📞 Phone Info:")
        phone_data, error = get_phone_info(phone_number)
        if error:
            print(error)
        else:
            print(f"Formatted       : {phone_data['Formatted']}")
            print(f"Location        : {phone_data['Location']}")
            print(f"Carrier         : {phone_data['Carrier']}")

        print("\n📡 CallTracer Info (if available):")
        ct_data = trace_calltracer_info(phone_number)
        if ct_data:
            for key, val in ct_data.items():
                print(f"{key:17}: {val}")
        else:
            print("ℹ️  No CallTracer data found or unable to fetch.")

        # Links
        clean_number = phone_number.replace("+", "").strip()
        print("\n🌐 Quick Links:")
        print(f"WhatsApp Chat   : https://wa.me/{clean_number}")
        print(f"Telegram Link   : https://t.me/+{clean_number}\n")

# Run the script
if __name__ == "__main__":
    main()