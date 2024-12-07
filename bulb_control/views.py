from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import africastalking
import urllib.parse
from django.shortcuts import render
from .models import Bulb
import logging

logger = logging.getLogger(__name__)


username = "simalert"  
api_key = "atsk_6f8d5e4a837a68cfaccfa81922360f5e6d7e3082e0aca4a01314c2857ffe833ff25fda59"  
africastalking.initialize(username, api_key)
sms_service = africastalking.SMS

@csrf_exempt
def sms_webhook(request):
    """
    Handles incoming SMS messages from Africa's Talking.
    """
    if request.method == "POST":
        try:
            logger.info(f"Request body: {request.body}")
            
           
            data = urllib.parse.parse_qs(request.body.decode('utf-8'))
            logger.info(f"Parsed data: {data}")

            
            message = data.get('text', [''])[0].strip().lower()
            sender = data.get('from', [''])[0]

           
            bulb, _ = Bulb.objects.get_or_create(id=1)

         
            if message == "switch on":
                bulb.state = True
                response_message = "Bulb has been switched ON."
            elif message == "switch off":
                bulb.state = False
                response_message = "Bulb has been switched OFF."
            else:
                response_message = "Invalid command. Use 'switch on' or 'switch off'."

            
            bulb.save()

           
            send_sms(sender, response_message)

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            logger.error(f"Error processing SMS: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


def send_sms(to, message):
    """
    Sends an SMS message using Africa's Talking.
    """
    try:
        response = sms_service.send(message, [to])
        logger.info(f"SMS sent: {response}")
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")


@csrf_exempt
def bulb_status(request):
    """
    Returns the current status of the bulb.
    """
    bulb, _ = Bulb.objects.get_or_create(id=1)
    return JsonResponse({"state": bulb.state})


@csrf_exempt
def toggle_bulb(request):
    """
    Toggles the state of the bulb.
    """
    if request.method == "POST":
        bulb, _ = Bulb.objects.get_or_create(id=1)
        bulb.state = not bulb.state
        bulb.save()
        return JsonResponse({"state": bulb.state})
    return JsonResponse({"error": "Invalid request method."}, status=400)


def home(request):
    """
    Renders the home page.
    """
    return render(request, 'index.html')
