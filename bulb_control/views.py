# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import africastalking
import json
from django.shortcuts import render
from .models import Bulb

username = "sim_alert" 
api_key = "atsk_6f8d5e4a837a68cfaccfa81922360f5e6d7e3082e0aca4a01314c2857ffe833ff25fda59"   
africastalking.initialize(username, api_key)
sms_service = africastalking.SMS

@method_decorator(csrf_exempt, name='dispatch')
def sms_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get('text', '').strip().lower()  
            sender = data.get('from', '')  

            bulb, created = Bulb.objects.get_or_create(id=1)  
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