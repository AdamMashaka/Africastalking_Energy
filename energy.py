from flask import Flask, request
import africastalking
import os
import requests

app = Flask(__name__)

# Initialize Africastalking
username = "sandbox"
api_key = "atsk_0bba4b807c90e26c930cc206d384414f2d38038b717718bc0a1a6801d23a"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    # Extract USSD request data
    session_id = request.values.get("sessionId", "")
    service_code = request.values.get("serviceCode", "")
    phone_number = request.values.get("phoneNumber", "")
    text = request.values.get("text", "")

    response = ""

    # Main Menu
    if text == "":
        response = (
            "CON Welcome to Energy conversation!\n"
            "Your one-stop solution for various services:\n"
            "1. Buy Electricity\n"
            "2. View Weekly Electricity Footprint\n"
            "3. Contact Us\n"
            
        )

    # Electricity Options
    elif text == "1":
        response = "CON Enter your electricity meter number:"

    elif text.startswith("1*"):
        meter_number = text.split('*')[1]
        response = (
            f"CON Meter {meter_number} detected.\n"
            "Select the amount to purchase:\n"
            "1. 5,000 TZS\n"
            "2. 10,000 TZS\n"
            "3. 20,000 TZS\n"
        )

    elif text == "2":
        response = (
            "END Your weekly electricity footprint:\n"
            "- Total Usage: 50 kWh\n"
            "- Estimated Cost: 15,000 TZS\n"
            "Tips: Reduce usage during peak hours to save costs."
        )

    # Contact Us
    elif text == "3":
        response = (
            "CON Choose a contact method:\n"
            "1. Call Us\n"
            "2. Send SMS\n"
            "3. Email Support\n"
        )

    elif text == "3*1":
        response = "END Call us at +255713581041 for support."

    elif text == "3*2":
        response = "END Send your query via SMS to +255713581041."

    elif text == "3*3":
        response = "END Email us at support@mapato.ai."

    # Agricultural Product Prices
    elif text == "4":
        response = (
            "CON Select a product to check prices:\n"
            "1. Maize\n"
            "2. Beans\n"
            "3. Rice\n"
            "4. Potatoes\n"
        )

    # Farming Advice
    elif text == "5":
        response = (
            "CON Choose a farming advice topic:\n"
            "1. Crop Planting\n"
            "2. Pest Control\n"
            "3. Soil Improvement\n"
            "4. Harvesting & Storage\n"
        )

    elif text == "6":
        response = (
            "END Today's weather update:\n"
            "- Temperature: 30°C\n"
            "- Rainfall: 10mm\n"
            "- Wind Speed: 5km/h\n"
        )

    else:
        response = "END Invalid input. Please try again."

    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
