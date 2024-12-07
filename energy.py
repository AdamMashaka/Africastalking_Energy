from flask import Flask, request 
import africastalking 
import os
import requests 


app = Flask(__name__)
username = "sandbox"
api_key = "atsk_0bba4b807c90e26c930cc206d384414f2d38038b717718bc0a1a6801d23a"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response_1, response_2
    session_id = request.values.get("sessionId", "atsk_d65b63bd0ac289c10ac7e4cf16747915b1733bb096aebaa905af0776ce74a60222b7d1")
    service_code = request.values.get("serviceCode", "*384#")
    phone_number = request.values.get("phoneNumber", +255694021848)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    response = ""

    #ussd logic
    if text == "":
        #main menu
        response = "CON Karibu MAPATO AI Kupata Huduma Kuhusu KILIMO:\n"
        "/n"
        response += "Chagua sehemu unayotaka:\n"
        response += "1. Habari kuhusu Bei ya Mazao\n"
        response += "2. Ushauri wa Kilimo\n"
        response += "3. Habari kuhusu Hali ya hewa\n"
        response += "4. Mnunuzi\n"
        response += "5. Msaada wa Kiufundi\n"

    elif text == "1":
        #sub menu 1
        response = "CON Chagua Mazao unayotaka kujua Bei\n"
        response += "1. Mahindi\n"
        response += "2. Maharage\n"
        response += "2. Mchele\n"
        response += "3. Viazi \n"
        response += "4. Uwele\n"
        response += "5. Ulezi\n"
        response += "6. Mtama\n"
        response += "7. Ngano\n"

    elif text == "1*1":
        response = "CON Ingiza eneo lako la kilimo la mahindi"
    elif text.startswith("1*1"):
        location = text.split('*')[2]

        maize_price = get_maize_price(location)

        if maize_price:
            response = f"END Bei ya mahindi katika eno lako la {location} ni {maize_price} TSH/100kg "
            try:
                # sending msg
                sms_response = sms.send(f"Bei ya mahindi katika eno lako la {location} ni {maize_price} TSH/100kg ", sms_phone_number)
                print(sms_response)
                # catching error
            except Exception as e:
                print("There is fucking Error {}".format(e))
        else:
             response = f"END Kama Bei ya mahindi ikipanda au kupungua Tutaujurisha Mpendwa "

    elif text == "1*2":
        response = "CON Ingiza eneo lako la kilimo la maharage"         
    elif text.startswith("1*2*"):
        location = text.split('*')[2]

        beans_price = get_beans_price(location)

        if beans_price:
            response = f"END Bei ya maharage katika eneo lako la {location} ni {beans_price} TSH/100kg"

            try:
                # sending msg
                sms_response = sms.send(
                    f"Bei ya maharage katika eno lako la {location} ni {beans_price} TSH/100kg ",
                    sms_phone_number)
                print(sms_response)
                # catching error
            except Exception as e:
                print("There is fucking Error {}".format(e))
        else:
            response = f"END Kama Bei ya maharage ikipanda au kupungua Tutakujurisha Mpendwa "

    elif text == "1*3":
        response = "CON Ingiza eneo lako la kilimo la viazi"  

    elif text.startswith("1*3"):
        location = text.split('*')[2]

        potato_price = get_potato_price(location)

        if potato_price:
            response = f"END Bei ya viazi katika eneo lako la {location} ni {potato_price} TSH/kg"

            try:
                # sending msg
                sms_response = sms.send(
                    f"Bei ya Viazi katika eno lako la {location} ni {potato_price} TSH/100kg ",
                    sms_phone_number)
                print(sms_response)
                # catching error
            except Exception as e:
                print("There is fucking Error {}".format(e))
        else:
            response = f"END Kama Bei ya Viazi ikipanda au kupungua Tutakujurisha Mpendwa "

    elif text.startswith("1*4")  :
        location = text.split("*") [2]
        uwele_price = get_uwele_price(location)

        if uwele_price:
            response = f"END Bei ya Uwele katika eneo lako la {location} ni {uwele_price} TSH/100kg"
        try:
            # sending msg
            sms_response = sms.send(
                f"Bei ya Uwele katika eno lako la {location} ni {uwele_price} TSH/100kg ",
                sms_phone_number)
            print(sms_response)
            # catching error
        except Exception as e:
         print("There is fucking Error {}".format(e))
        else:
          response = f"END Kama Bei ya Uwele ikipanda au kupungua Tutakujurisha Mpendwa "

    elif text.startswith("1*5"):
        location = text.split("*")[3]
        ulezi_price = get_ulezi_price(location)

        if ulezi_price:
            response = f"END Bei ya Ulezi katika eneo lako la {location} ni {ulezi_price} TSH/100kg"
        try:
            # sending msg
            sms_response = sms.send(
                f"Bei ya Ulezi katika eno lako la {location} ni {ulezi_price} TSH/100kg ",
                sms_phone_number)
            print(sms_response)
            # catching error
        except Exception as e:
            print("There is fucking Error {}".format(e))


        else:
            response = f"END Kama Bei ya Ulezi ikipanda au kupungua Tutakujurisha Mpendwa "


    elif text.startswith("1*6"):
        location = text.split("*")[2]
        mtama_price = get_mtama_price(location)

        if mtama_price:
            response = f"END Bei ya Mtama katika eneo lako la {location} ni {mtama_price} TSH/100kg"
        try:
            # sending msg
            sms_response = sms.send(
                f"Bei ya Mtama katika eno lako la {location} ni {mtama_price} TSH/100kg ",
                sms_phone_number)
            print(sms_response)
            # catching error
        except Exception as e:
            print("There is fucking Error {}".format(e))

        else:
            response = f"END Kama Bei ya Mtama ikipanda au kupungua Tutakujurisha Mpendwa "


    elif text.startswith("1*7"):
        location = text.split("*")[2]
        ngano_price = get_ngano_price(location)

        if ngano_price:
            response = f"END Bei ya Ngano katika eneo lako la {location} ni {ngano_price} TSH/100kg"
        try:
            # sending msg
            sms_response = sms.send(
                f"Bei ya Ngano katika eno lako la {location} ni {ngano_price} TSH/100kg ",
                sms_phone_number)
            print(sms_response)
            # catching error
        except Exception as e:
            print("There is fucking Error {}".format(e))


        else:
            response = f"END Kama Bei ya Ngano ikipanda au kupungua Tutakujurisha Mpendwa "

    elif text == "2":
        response = "CON Karibu kwenye Huduma ya Ushauri wa Kilimo.\n"
        response += "Tafadhali chagua chaguo:\n"
        response += "1. Ushauri wa Upandaji Mazao\n"
        response += "2. Ushauri wa Kudhibiti Wadudu\n"
        response += "3. Ushauri wa Kuboresha Udongo\n"
        response += "4. Ushauri wa Kuvuna na Kuhifadhi"

    elif text == "2*1":
        response =  "END USHAURI WA UPANDAJI WAMAZAO:\n"
        response += "- Tumia mbegu bora na zenye ubora ilikupata mazao mazuri\n"
        response += "- Tumia mbolea kulingana na mahitaji ya mazao yako\n"
        response += "- Panda kwa kuzingatia mpangilio na umbali sahihi\n"
        response += "- Fanya umwagiliaji wa kutosha na salama\n"
        response += "- Kwa ushauri zaidi wasiliana nasi kupitia namba +255689737839"

        try:
           #sending msg
           sms_response = sms.send(response, sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e)) 

    elif text == '2*2':
        # Ushauri wa Kudhibiti Wadudu
        response = "END Ushauri wa kudhibiti wadudu:\n"
        response += "- Chagua njia ya kudhibiti wadudu inayofaa kwa mazao yako\n"
        response += "- Tumia dawa za kudhibiti wadudu kwa usahihi na kwa kipimo sahihi\n"
        response += "- Fanya ufuatiliaji wa mara kwa mara na udhibiti wadudu mapema"

        try:
           #sending msg
           sms_response = sms.send(response, sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e)) 

    elif text == '2*3':
        # Ushauri wa Kuboresha Udongo
        response = "END Ushauri wa kuboresha udongo:\n"
        response += "- Tumia mbolea za kikaboni kama mboji na kome\n"
        response += "- Pima pH ya udongo na kurekebisha ikiwa ni lazima\n"
        response += "- Panda mazao ya kujilisha udongo kama vile maharage na mikunde\n"
        response += "- Fanya mzunguko wa mazao"

        try:
           #sending msg
           sms_response = sms.send(response, sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e)) 

    elif text == '2*4':
        # Ushauri wa Kuvuna na Kuhifadhi
        response = "END Ushauri wa kuvuna na kuhifadhi:\n"
        response += "- Kusanya mazao kwa wakati unaofaa na kwa njia sahihi\n"
        response += "- Hifadhi mazao katika mazingira safi na yenye ubora\n"
        response += "- Weka tahadhari dhidi ya wadudu na kuoza kwa mazao"

        try:
           #sending msg
           sms_response = sms.send( "Ushauri wa kuvuna na kuhifadhi:\n"
         "** Kusanya mazao kwa wakati unaofaa na kwa njia sahihi\n"
         "** Hifadhi mazao katika mazingira safi na yenye ubora\n"
         "** Weka tahadhari dhidi ya wadudu na kuoza kwa mazao"
                                                               , sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e)) 


    elif text == "5":
        response = "CON Chagua njia ya kuwasiliana na msaada wa kiufundi:\n"
        response += "1. Piga Simu\n"
        response += "2. Tuma Ujumbe\n"
        response += "3. Barua pepe\n"

    elif text == "5*1":
        response = "END Piga simu kwa watalaamu wetu wakilimo kwa namba +255713581041."
        
        try:
           #sending msg
           sms_response = sms.send("Piga simu kwa watalaamu wetu wakilimo kwa namba +255713581041.", sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e)) 

    elif text == "5*2":
        response = "END Tuma ujumbe kwa watalaamu wetu wa kilimo kwa namba +255689737839."
        
        try:
           #sending msg
           sms_response = sms.send(response, sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e)) 

    elif text == "5*3":
        response = "END Tuma barua pepe kwa watalaamu wetu wa kilimo kwa anwani smartshambaspecialist@live.com."
        
        try:
           #sending msg
           sms_response = sms.send("Tuma barua pepe kwa watalaamu wetu wa kilimo kwa anwani smartshambaspecialist@live.com.", sms_phone_number)
           print(sms_response)
           #catching error
        except Exception as e:
            print("There is fucking Error {}".format(e))

    elif text == '4':
        # Mkulima Mnunuzi
        response = "CON Chagua chaguo:\n"
        response += "1. Tafuta Mazao\n"
        response += "2. Nunua Mazao"
    elif text == '4*1':
        # Tafuta Mazao
        response = "CON Ingiza jina la mkoa:\n"
    elif text.startswith('4*1*'):
        # Tafuta Mazao kulingana na mkoa
        region = text.split('*')[2]
        crops = get_crops_by_region(region)
        if crops:
            response = f"END Mazao yaliyopo katika mkoa wa {region} ni:\n"
        for crop in crops:
            response += f"- {crop}\n"

        try:
            # sending msg
            sms_response = sms.send(response, sms_phone_number)
            print(sms_response)
            # catching error
        except Exception as e:
            print("There is fucking Error {}".format(e))


        else:
            response = "END Hakuna mazao yaliyopatikana katika mkoa huo."
    elif text == '4*2':
        # Nunua Mazao
        response = "CON Ingiza jina la mazao unayotafuta:\n"
    elif text.startswith('4*2*'):
        # Nunua Mazao kulingana na jina la mazao
        crop_name = text.split('*')[2]
        sellers = get_sellers_by_crop(crop_name)
        if sellers:
            response = f"END Wauzaji wa {crop_name} ni:\n"
        for seller in sellers:
            response += f"- {seller['name']}: {seller['phone']}\n"

        try:
            # sending msg
            sms_response = sms.send(response, sms_phone_number)
            print(sms_response)
            # catching error
        except Exception as e:
            print("There is fucking Error {}".format(e))



        else:
            response = "END Hakuna wauzaji walioorodheshwa kwa mazao hayo."



    else:
        # Uingiaji usiofaa
         response = "END Uingiaji usiofaa. Tafadhali chagua chaguo sahihi."
    
    return response
    
def get_maize_price(location):
    if location == "Arusha":
        return "100,000"
    
    else:
        return None

def get_beans_price(location):
    # Bei ya maharage kulingana na eneo
    if location == "Arusha":
        return "100,000"
    elif location == "Dar es Salaam" or "Daresalaam" or "DSM":
        return "95,000"
    elif location == "Mbeya" or "mbeya":
        return "95,000"
    elif location == "Dodoma":
        return "88,000"
    
    else:
        return None

def get_potato_price(location):
    # Bei ya viazi kulingana na eneo
    if location == "Arusha":
        return "115,000"
   
    elif location == "katavi":
        return "70,000"

    else:
        return None

def get_uwele_price(location):
    if location == "Arusha":
        return "100,000"
    elif location == "Dar es Salaam" or "Daresalaam" or "DSM":
        return "95,000"
    elif location == "Mbeya" or "mbeya":
        return "95,000"
    
    elif location == "Iringa":
        return "90,000"
    else:
        return None
def get_ulezi_price(location):
    if location == "Arusha":
        return "100,000"
    else:
        return None

def get_mtama_price(location):
    if location == "Arusha":
        return "100,000"
    elif location == "Dar es Salaam" or "Daresalaam" or "DSM":
        return "95,000"
    elif location == "Mbeya" or "mbeya":
        return "95,000"
    
    else:
        return None

def get_ngano_price(location):
    if location == "Arusha":
        return "100,000"
    elif location == "Dar es Salaam" or "Daresalaam" or "DSM":
        return "95,000"
    
    else:
        return None
# Mantiki ya kupata wauzaji kulingana na jina la mazao (data hardcoded)
def get_sellers_by_crop(crop_name):
    if crop_name == 'Mahindi':
        sellers = [
            {"name": "Mkojani Kazola", "phone": "+255713581041"},

        ]
    elif crop_name == 'Mpunga':
        sellers = [
            {"name": "Mkulima 3", "phone": "+255613581290"},

        ]
    elif crop_name == 'Maharage':
        sellers = {
            {"name": "Mkulima 5", "phone": "+255713581041"},

        }

    elif crop_name == 'Mchele':
        sellers = [
            {"name": "Mkulima 5", "phone": "+255713581041"},
    

        ]

    elif crop_name == 'Viazi':
        sellers = [
            {"name": "Mkulima 5", "phone": "+255713581041"},
            

        ]

    else:
        sellers = []
    return sellers

def get_crops_by_region(region):
    if region == 'Arusha':
        crops = ["Mahindi", "Mpunga"]
    else:
        crops = []
    return crops



def get_weather_data(location):
    # Pata taarifa ya hali ya hewa kutoka OpenWeather API
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": '208912e57d4dc5b2cbd3060ef955416a',
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
            return weather_data
        else:
            return None

    except requests.exceptions.RequestException:
        return ("There is the fucking error here ")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))