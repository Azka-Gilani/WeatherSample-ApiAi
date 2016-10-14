#!/usr/bin/env python

import urllib
import json
import os

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

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    baseurl = "https://fazendanatureza.com/bot/botarz.php"
    r = requests.get(baseurl)
    data = r.json()
    #yql_url = baseurl
    #print(yql_url)
    #result = urllib.urlopen(yql_url).read()
    #print("yql result: ")
    #print(result)

    #data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    query = data.get('title')
    if query is None:
        return {}
    # print(json.dumps(item, indent=4))

    speech="Testing"+ query

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": "testing",
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
