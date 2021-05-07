import requests
import datetime
import json
import pandas as pd
import smtplib
import os
#for state_code in range(1,40):
#    print("State code: ", state_code)
#    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code))
#    json_data = json.loads(response.text)
#    for i in json_data["districts"]:
#        print(i["district_id"],'\t', i["district_name"])
#    print("\n")

DIST_ID = 294 # Bangalore BBMP
#DIST_ID = 265 # Bangalore Urban
#DIST_ID = 363 #Pune
#DIST_ID = 141 #Delhi

# Print available centre description (y/n)?
print_flag = 'y'

numdays = 30
age = 18


base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]


for INP_DATE in date_str:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
    response = requests.get(URL)
    if response.ok:
        resp_json = response.json()
        #print(json.dumps(resp_json, indent = 1))
        if resp_json["centers"]:
            #print("Available on: {}".format(INP_DATE))
            if(print_flag=='y' or print_flag=='Y'):
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age and session["vaccine"] != '' and session["available_capacity"] != 0:
                            print("Available for:", session["min_age_limit"], "years old and above ,", "Available on: {}".format(INP_DATE), ",", "Hospital/PHC Name:", center["name"], ",", "Area/Block Name:",center["block_name"], ",", "Price:",center["fee_type"], ",", "Available Capacity:",session["available_capacity"], ",", "Vaccine: ", session["vaccine"] )
                            #print("\t", center["block_name"])
                            #print("\t Price: ", center["fee_type"])
                            #print("\t Available Capacity: ", session["available_capacity"])
                            #if(session["vaccine"] != ''):
                                #print("\t Vaccine: ", session["vaccine"])
                            print("\n\n")
                            li = ["emailid1", "emailid2"]
                            for dest in li:
                                s = smtplib.SMTP('smtp.gmail.com', 587)
                                s.starttls()
                                s.login("sender's gmail email id here", "gmail password")
                                message = "please check covid vaccine slots available in Bangalore. you can add here vaccine information as well"
                                s.sendmail("sender's gmail email id here", dest, message)
                                s.quit()
                                #print("test")



        else:
            print("No available slots on {}".format(INP_DATE))
