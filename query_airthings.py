"""
Quick way to query the AirThings API and
import that output into a Grafana dashboard.
"""

import json
import requests

AUTHURL = "https://accounts-api.airthings.com/v1/token"
DEVICEURL = "https://ext-api.airthings.com/v1/devices"


# Setup the Client secrets
authPayload = json.dumps({
  "grant_type": "client_credentials",
  "client_id": "{$ CLIENT ID }",
  "client_secret": "{$ CLIENT SECRET } ",
  "scope": [
    "read:device:current_values"
  ]
})
authHeaders = {
  'Content-Type': 'application/json'
}

# Login
auth = requests.request("POST", AUTHURL, headers=authHeaders, data=authPayload, timeout=3)
authJSON = auth.json()
authToken = authJSON.get('access_token')

requestHeader = {
  "Authorization": 'Bearer ' + authToken
}

# Get the device list
devices = requests.get(url=DEVICEURL, headers = requestHeader, timeout = 10)
devicesJSON = devices.json()

data = []

for deviceIds in devicesJSON["devices"]:
  if deviceIds["deviceType"] == "WAVE_PLUS":
    deviceid = deviceIds["id"]

    # Query for the devices stats
    stats = requests.get(url='https://ext-api.airthings.com/v1/devices/' + deviceid + '/latest-samples', headers = requestHeader, timeout = 10)
    statsJSON = stats.json()

    # Format the data for influxDB, adding the deviceId to the output
    dictOutput = json.loads('{ "deviceid": ' + deviceid + ',' + json.dumps(statsJSON["data"]).strip('{}') + '}')

    #formattedData = json.loads(jsonOutput)
    data.append(dictOutput)

# Output the data
print(json.dumps(data, indent=4))
