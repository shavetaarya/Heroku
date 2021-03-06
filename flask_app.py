#!/usr/bin/env python

import urllib
import json
import os
import pandas as pd
import csv

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
#    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "KMS_read":
       result = req.get("result")
       context = result.get("contexts")
       context = json.dumps(context, indent=4)
       context = json.loads(context)
       print(context)
       parameters = (context[0]['parameters'])
       print(parameters)
       number = parameters.get("number")
       print(number)
       check_no = 'Check ' + str(number)
       KMS = ("KMS1.csv")
       with open(KMS) as csvfile:
          reader = csv.reader(csvfile,delimiter=',')
          for row in reader:
            if check_no == row[0]:
               print(row[1])
               speech=row[1]
               break 
            else:
               speech = 'I will not be able to help you with this query. Please contact human operator at +91-123456789' 
    
    
    if req.get("result").get("action") == "trade_desc":
       result = req.get("result")
       trade_id = result.get("resolvedQuery")
       print(trade_id)
       trade_df = ("trade.csv")
       with open(trade_df) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            if trade_id == row[0]:
               print(row[1])
               speech='This deal was executed by ' + row[2] + ' For counterparty '+ row[3] + ' On date ' + row[1] + ' Currency Pair: ' + row[4] + ' And deal amount is ' + row[5]
               break 
            else:
                speech = 'I am not be able to find this TRADE ID. Please contact human operator at +91-123456789' 
#    cost = {'Andhra Bank':'6.85%', 'Allahabad Bank':'6.75%', 'Axis Bank':'6.5%', 'Bandhan bank':'7.15%', 'Bank of Maharashtra':'6.50%', 'Bank of Baroda':'6.90%', 'Bank of India':'6.60%', 'Bharatiya Mahila Bank':'7.00%', 'Canara Bank':'6.50%', 'Central Bank of India':'6.60%', 'City Union Bank':'7.10%', 'Corporation Bank':'6.75%', 'Citi Bank':'5.25%', 'DBS Bank':'6.30%', 'Dena Bank':'6.80%', 'Deutsche Bank':'6.00%', 'Dhanalakshmi Bank':'6.60%', 'DHFL Bank':'7.75%', 'Federal Bank':'6.70%', 'HDFC Bank':'5.75% to 6.75%', 'Post Office':'7.10%', 'Indian Overseas Bank':'6.75%', 'ICICI Bank':'6.25% to 6.9%', 'IDBI Bank':'6.65%', 'Indian Bank':'4.75%', 'Indusind Bank':'6.85%', 'J&K Bank':'6.75%', 'Karnataka Bank':'6.50 to 6.90%', 'Karur Vysya Bank':'6.75%', 'Kotak Mahindra Bank':'6.6%', 'Lakshmi Vilas Bank':'7.00%', 'Nainital Bank':'7.90%', 'Oriental Bank of Commerce':'6.85%', 'Punjab National Bank':'6.75%', 'Punjab and Sind Bank':'6.4% to 6.80%', 'Saraswat bank':'6.8%', 'South Indian Bank':'6% to 6.75%', 'State Bank of India':'6.75%', 'Syndicate Bank':'6.50%', 'Tamilnad Mercantile Bank Ltd':'6.90%', 'UCO bank':'6.75%', 'United Bank Of India':'6%', 'Vijaya Bank':'6.50%', 'Yes Bank':'7.10%'}
#
#    speech = "The interest rate of " + zone + " is " + str(cost[zone])
#    speech = str((error_data['Resolution'] ))
    print(speech)
    print("Response:")
    print("This is the reply from Python webhook"  )
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
#        "source": "BankRates"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')