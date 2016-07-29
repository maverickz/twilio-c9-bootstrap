import requests
import json
import difflib
import requests
import re

from copy import copy
from flask import Flask, request
from pprint import pprint
from HTMLParser import HTMLParser


app = Flask(__name__)

config_file = open('../config.json', 'r')
config = json.load(config_file)

ACCOUNT_SID = config['account_sid']
AUTH_TOKEN = config['auth_token']

CHAR_LIST_ENDPOINT='http://api.viewers-guide.hbo.com/service/charactersList'
DETAIL_ENDPOINT='http://api.viewers-guide.hbo.com/service/characterDetails'
DEFAULT_PARAMS = {'lang': 1}

listresp = requests.get(CHAR_LIST_ENDPOINT, DEFAULT_PARAMS)
characters_list = listresp.json()
first_names = [ character['firstname'].lower() for character in characters_list ] 
last_names = [ character['lastname'].lower() for character in characters_list ]
full_names = [first_names[i] + ' ' + last_names[i] for i in xrange(len(first_names))]

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
 
@app.route('/get_char_desc', methods=['GET', 'POST'])
def get_char_desc():
    first_name = ''
    last_name = ''
    name = ''
    names = request.values.get('Body').split()
    if len(names) > 1:
        first_name = names[0]
        last_name = names[1]
    else:
        name = names[0]
    
    char_id = None
    
    for character in characters_list:
        if not last_name:
            if name.lower() == character['firstname'].lower() or name.lower() == character['lastname'].lower():
                char_id = character['id']
                break
        else:
            if first_name.lower() == character['firstname'].lower() and last_name.lower() == character['lastname'].lower():
                char_id = character['id']
                break
        
    if char_id is not None:
        extra_params = copy(DEFAULT_PARAMS)
        extra_params['id'] = char_id
        response = requests.get(DETAIL_ENDPOINT, extra_params)
        char_desc = response.json()['bio']['body']
        char_desc = strip_tags(char_desc)
        print char_id, char_desc
        return """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
           <Sms>""" + char_desc + """</Sms>
        </Response>"""
    else:
        matches = ''
        if not last_name:
            matches = find_closest_match(name.lower())
        else:
            matches = find_closest_match(first_name.lower() + ' ' + last_name.lower(), match_list=full_names)
        message = ''
        if not matches:
            message = 'Sorry character not available'
        else: 
            message = 'Name not found. Did you mean %s' % matches
        return """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
           <Sms>""" + message + """</Sms>
        </Response>"""
 
def find_closest_match(name, match_list=None, num_matches=5):
    matching_names = []
    if match_list is None:
        closest_matches = difflib.get_close_matches(name, first_names, n=num_matches, cutoff=0.6)
        for first_name in closest_matches:
            matching_names.append(first_name + ' ' + last_names[first_names.index(first_name)])
        if len(closest_matches) < num_matches:
            more_matches = difflib.get_close_matches(name, last_names, n=num_matches, cutoff=0.6)
            for last_name in more_matches:
                matching_names.append(first_names[last_names.index(last_name)] + ' ' + last_name)
    else:
        matching_names = difflib.get_close_matches(name, match_list, n=num_matches, cutoff=0.6)
        
    return ', '.join(matching_names).title()

def strip_html(text):
    return re.sub('<[^<]+?>', '', text)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
