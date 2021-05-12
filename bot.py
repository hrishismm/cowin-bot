from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from urllib.request import urlopen
import json
import requests
import emoji
import re

def isValidPinCode(pinCode):
      
    # Regex to check valid pin code
    # of India.
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"; 
  
    # Compile the ReGex 
    p = re.compile(regex);
      
    # If the pin code is empty
    # return false
    if (pinCode == ''):
        return False;
          
    # Pattern class contains matcher() method
    # to find matching between given pin code
    # and regular expression.
    m = re.match(p, pinCode);
      
    # Return True if the pin code
    # matched the ReGex else False
    if m is None:
        return False
    else:
        return True

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()
    """Respond to whatsapp messages"""
    # Fetch the message
   
    #print(json_text)
    #Create reply
    resp = MessagingResponse()
    if incoming_msg == 'hello':
            response = emoji.emojize("""
*Hi! I am the Cowin Bot* :wave:
Let's be friends :wink:
You can give me the following command:
:black_small_square: *'pincode-<yourpincode>':* Get info about the available slots at the vaccination center near you! 
""", use_aliases=True)
            resp.message(response)
            responded = True
    
    
    
    if incoming_msg.startswith('pincode'):
        test=incoming_msg.partition("pincode-")[2]
        print(test)
        if(isValidPinCode(test)):
                headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
                r = requests.get(url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+test+"&date=12-05-2021",headers=headers)
                json_text=r.text
                json_text=json.loads(json_text)
                try:
                    for i in range(0,100):
                        center=json_text['centers'][i]
                        
                        resp.message("Center Name:"+center['name']+
                        "\n"+"Address:"+center['address']
                        +"\n"+"State:"+center['state_name']
                        +"\n"+"District:"+center['district_name']+
                        "\n"+"Block name:"+center['block_name']+
                        "\n"+"From:"+center['from']+"\n"+"To:"+center['to']+"\n"+
                        "Date:"+center['sessions'][0]['date']+"\n"+
                        "Vaccine:"+center['sessions'][0]['vaccine']+"\n"+
                        "Min_Age_Limit:"+str(center['sessions'][0]['min_age_limit'])+"\n"+
                        "Available Vaccines:"+str(center['sessions'][0]['available_capacity']))
                            
                except:
                    print("Out of Index")
        
    msg = request.form.get('Body')
    #print(format(msg))
    
    
    

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)