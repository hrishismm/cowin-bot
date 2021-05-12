import requests
import json

res=requests.post("https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP", json={"mobile": "9670000000"})

print(res)
json_text=res.text

print(type(json_text))

print(json_text)
print(json_text[10:-2])