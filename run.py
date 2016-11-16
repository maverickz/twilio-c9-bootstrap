#!/usr/bin/env python

from flask import Flask, request, redirect
from pprint import pprint
from twilio.rest import TwilioRestClient
from datetime import date, datetime
import twilio.twiml
import json
import csv
import os

MYDIR = os.path.dirname(__file__)

# Read account sid and auth token from environmental variables
ACCOUNT_SID = os.getenv("ACCOUNT_SID", "")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

app = Flask(__name__)

def get_birthday_list_from_file():
    with open(os.path.join(MYDIR, 'birthdays.csv'), 'rb') as fp:
        reader = csv.reader(fp)
        birthday_list = list(reader)
    return birthday_list

def find_matching_contact_detail(birthday_list, phone_number):
    for contact_detail in birthday_list:
        if phone_number == contact_detail[4]:
            return contact_detail
    return None
 
@app.route("/sms", methods=['POST'])
def receive_message():
    """Respond to incoming calls with a simple text message."""
    pprint(request.values)
    text_response = request.values.get("Body")
    phone_number = request.values.get("From")
    birthday_list = get_birthday_list_from_file

    contact_detail = find_matching_contact_detail(birthday_list, phone_number)

    first_name = phone_number
    last_name = ""

    if contact_detail is not None:
        first_name = contact_detail[0]
        last_name = contact_detail[1]

    resp = "{} {} sent {}".format(first_name, last_name, text_response)
    client.messages.create(to="+16144775689", from_="+14152003278", body=resp)
    print("Response received from {} {}".format(first_name, last_name))
    # resp = twilio.twiml.Response()
    # resp.message("Hello, Mobile Monkey")
    # return str(resp)
 
@app.route("/sms", methods=['GET'])    
def send_birthday_message():
    """Parses csv file and sends birthday message for people whose birthday falls on the current day"""
    
    birthday_list = get_birthday_list_from_file()

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
    port = os.getenv("PORT", 8080)	
    app.run(debug=True, host='0.0.0.0', port=int(port))
