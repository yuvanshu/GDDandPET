#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from builtins import str
from builtins import bytes
from builtins import object

import requests as rq
import base64
import pprint
import json
import os
import random
import datetime

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template


# Flask app should start in global layout

app = Flask(__name__)

@app.route('/hello')
def hello():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print('Request:')
    #print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access. 
    req_dict = json.loads(request.data)
    
    parameters = req_dict["result"]["parameters"]
    
    date = parameters["date"]
    crop = parameters["crop"]

    # constructing the resposne string.
    speech = "GDD for " + crop + " as of " + date 
    res = makeWebhookResult(speech)
    return res


def makeWebhookResult(speech):
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "Build conversational interface for your app in 10 minutes."
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
