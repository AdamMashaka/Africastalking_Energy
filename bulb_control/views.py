from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import africastalking
import json
from django.shortcuts import render
from .models import Bulb

# Initialize Africa's Talking
username = "your_username"  # Replace with your Africa's Talking username
api_key = "your_api_key"    # Replace with your Africa's Talking API key
africastalking.initialize(username, api_key)
sms_service = africastalking.SMS

@method_decorator(csrf_exempt, name='dispatch')
def sms_webhook(request):
    if request.method == "POST":
        try:
            # Parse incoming SMS data
            data = json.loads(request.body)
            message = data.get('text', '').strip().lower()  # Incoming SMS content
            sender = data.get('from', '')  # Sender phone number

            # Bulb state handling
            bulb, created = Bulb.objects.get_or_create(id=1)  # Single bulb state
            if message == "switch on":
                bulb.state = True
                response_message = "Bulb has been switched ON."
            elif message == "switch off":
                bulb.state = False
                response_message = "Bulb has been switched OFF."
            else:
                response_message = "Invalid command. Use 'switch on' or 'switch off'."

            bulb.save()

            # Respond to the sender via Africa's Talking
            send_sms(sender, response_message)
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

def send_sms(to, message):
    try:
        response = sms_service.send(message, [to])
        print(f"SMS sent: {response}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

@csrf_exempt
def bulb_status(request):
    bulb, _ = Bulb.objects.get_or_create(id=1)
    return JsonResponse({"state": bulb.state})

@csrf_exempt
def toggle_bulb(request):
    if request.method == "POST":
        bulb, _ = Bulb.objects.get_or_create(id=1)
        bulb.state = not bulb.state
        bulb.save()
        return JsonResponse({"state": bulb.state})
    return JsonResponse({"error": "Invalid request method."}, status=400)

def home(request):
    return render(request, 'index.html')