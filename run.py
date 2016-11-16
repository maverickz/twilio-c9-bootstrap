#!/usr/bin/env python

from flask import Flask, request, redirect
from pprint import pprint
from twilio.rest import TwilioRestClient
from datetime import date, datetime
import twilio.twiml
import json
import csv
import os

config_file = open("/home/ubuntu/config.json", "r")
config = json.load(config_file)

ACCOUNT_SID = config["account_sid"]
AUTH_TOKEN = config["auth_token"]

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

app = Flask(__name__)
 
@app.route("/sms", methods=['GET', 'POST'])
def receive_message():
    """Respond to incoming calls with a simple text message."""
    pprint(request.values)
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)
    
def send_birthday_message():
    """Parses csv file and sends birthday message for people whose birthday falls on the current day"""
    
    with open('/home/ubuntu/workspace/birthdays.csv', 'rb') as fp:
        reader = csv.reader(fp)
        birthday_list = list(reader)

    today = date.today()
    print today
    for contact_detail in birthday_list:
        birthday = contact_detail[2]
        date_object = datetime.strptime(birthday, "%m/%d/%Y")
        
        # Check if the month and day matches the current month and day
        if date_object.month == today.month and date_object.day == today.day:
            birthday_message = contact_detail[3]
            phone_number = contact_detail[4]
            client.messages.create(to=phone_number, from_="+14152003278", body=birthday_message)
            print "Sent birthday wishes to " + contact_detail[0] 
 
if __name__ == "__main__":
    port = os.getenv('PORT', 8080)	
    app.run(debug=True, host='0.0.0.0', port=int(port))
