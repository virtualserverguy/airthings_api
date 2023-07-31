import json
import requests
import pandas as pd

authUrl = "https://accounts-api.airthings.com/v1/token"

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

deviceUrl = "https://ext-api.airthings.com/v1/devices"

# Login
auth = requests.request("POST", authUrl, headers=authHeaders, data=authPayload, timeout=3)
authJSON = auth.json()
authToken = authJSON.get('access_token')

requestHeader = {
  "Authorization": 'Bearer ' + authToken
}

# Get the device list
devices = requests.get(url=deviceUrl, headers = requestHeader)
devicesJSON = devices.json()

for deviceIds in devicesJSON["devices"]:
  if deviceIds["deviceType"] == "WAVE_PLUS":
    deviceid = deviceIds["id"]

    # Query for the devices stats
    stats = requests.get(url='https://ext-api.airthings.com/v1/devices/' + deviceid + '/latest-samples', headers = requestHeader)
    statsJSON = stats.json()

    # Format the data for influxDB, adding the deviceId to the output
    data = statsJSON["data"]
    data["deviceid"] = int(deviceid)

    # Output the data
    print(json.dumps(data))

  else:
    print("No WAVE PLUS devices found.")
