import requests
import datetime
import json
import pandas as pd
import smtplib
import os

POST_CODE = "560066"
age = 18

# Print details flag
print_flag = 'Y'

numdays = 30

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

for INP_DATE in date_str:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
        POST_CODE, INP_DATE)
    response = requests.get(URL)
    if response.ok:
        resp_json = response.json()
        #print(json.dumps(resp_json, indent = 1))
        flag = False
        if resp_json["centers"]:
            #print("Available on: {}".format(INP_DATE))
            if (print_flag == 'y' or print_flag == 'Y'):
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age and (session["vaccine"] != '') and (session["available_capacity"] != 0):
                            print("Available for:", session["min_age_limit"], "years old and above ,", "Available on: {}".format(INP_DATE), ",", "Hospital/PHC Name:", center["name"], ",", "Area/Block Name:",center["block_name"], ",", "Price:",center["fee_type"], ",", "Available Capacity:",session["available_capacity"], ",", "Vaccine: ", session["vaccine"] )
                            #print("\t", center["block_name"])
                            #print("\t Price: ", center["fee_type"])
                            #print("\t Available Capacity: ", session["available_capacity"])
                            #if (session["vaccine"] != ''):
                                #print("\t Vaccine: ", session["vaccine"])
                            print("\n\n")
                            li = ["emailid1", "emailid2"]
                            for dest in li:
                                s = smtplib.SMTP('smtp.gmail.com', 587)
                                s.starttls()
                                s.login("sender's gmail id", "gmail password")
                                message = "please check covid vaccine slots available in Whitefield. you can add vaccine info here"
                                s.sendmail("sender's gmail id", dest, message)
                                s.quit()
                                print("test")



        else:
            print("No available slots on {}".format(INP_DATE))



