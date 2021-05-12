import requests


r = requests.request(method='PUT',url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=400001&date=10-05-2021')




print(r.text)