# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 13:14:51 2018

@author: ashaveta
"""

#!/usr/bin/env python

import urllib
import json
import os
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
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "Number_Verify":
       result = req.get("result")
       context = result.get("contexts")
       context = json.dumps(context, indent=4)
       context = json.loads(context)
       print(context)
       parameters = (context[0]['parameters'])
       print(parameters)
       number = parameters.get("number")
       print(number)
       Customer = ("customer.csv")
       with open(Customer) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader: 
           print (row[0]) 
           if str(number) == str(row[0]):
               print(row)
               name = row[4]
               speech=("Welcome " + name + ", How May I help you today?")
               break 
           else:
               speech = 'I could not find this account number in my records. Please re-enter' 

        print(speech)
        print("Response:")
        print("This is the reply from Python webhook"  )
        return {
          "speech": speech,
          "displayText": speech,
        }
    if req.get("result").get("action") == "Balance_check":
       print ("checking balance")
       result = req.get("result")
       context = result.get("contexts")
       context = json.dumps(context, indent=4)
       context = json.loads(context)
       parameters = (context[0]['parameters'])
       number = parameters.get("number")
       print(number)
       Customer = ("customer.csv")
       with open(Customer) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader: 
           print (row[0]) 
           if str(number) == str(row[0]):
              speech=("Your account balance is " + row[1] + " $")
       print(speech)
       print("Response:")
       return {
          "speech": speech,
          "displayText": speech,
         }
    if req.get("result").get("action") == "loan_Amount":
       print ("checking loan due")
       result = req.get("result")
       context = result.get("contexts")
       context = json.dumps(context, indent=4)
       context = json.loads(context)
       parameters = (context[0]['parameters'])
       number = parameters.get("number")
       Customer = ("customer.csv")
       with open(Customer) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader: 
           print (row[0]) 
           if str(number) == str(row[0]):
              speech=("Your loan due this month is " + row[5] + " $ on " + row[6] )
       print(speech)
       print("Response:")
       return {
          "speech": speech,
          "displayText": speech,
         }
    if req.get("result").get("action") == "account_Spending":
       print ("checking spend")
       result = req.get("result")
       context = result.get("contexts")
       context = json.dumps(context, indent=4)
       context = json.loads(context)
       parameters = (context[0]['parameters'])
       number = parameters.get("number")
       Customer = ("customer.csv")
       with open(Customer) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader: 
           print (row[0]) 
           if str(number) == str(row[0]):
              speech=("Your total spend this month is " + row[3] + " $ "  )
       print(speech)
       print("Response:")
       return {
          "speech": speech,
          "displayText": speech,
         }
    if req.get("result").get("action") == "LC_expiry":
       print ("checking expiry")
       result = req.get("result")
       context = result.get("contexts")
       context = json.dumps(context, indent=4)
       context = json.loads(context)
       parameters = (context[0]['parameters'])
       number = parameters.get("number")
       Customer = ("customer.csv")
       with open(Customer) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader: 
           print (row[0]) 
           if str(number) == str(row[0]):
              speech=("Your LC Expiry date is " + row[2]   )
       print(speech)
       print("Response:")
       return {
          "speech": speech,
          "displayText": speech,
         }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')