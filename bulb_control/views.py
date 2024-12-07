from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from africastalking import AfricasTalkingGateway, AfricasTalkingGatewayException
import json
from .models import Bulb

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
    # Africa's Talking credentials
    username = "your_username"
    api_key = "your_api_key"

    gateway = AfricasTalkingGateway(username, api_key)

    try:
        gateway.sendMessage(to, message)
    except AfricasTalkingGatewayException as e:
        print(f"Error sending SMS: {e}")

