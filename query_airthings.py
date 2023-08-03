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
AuthHeaders = {
  'Content-Type': 'application/json'
}

# Login
Auth = requests.request("POST", AUTHURL, headers=AuthHeaders, data=authPayload, timeout=3)
AuthJSON = Auth.json()
AuthToken = AuthJSON.get('access_token')

RequestHeader = {
  "Authorization": 'Bearer ' + AuthToken
}

# Get the device list
Devices = requests.get(url=DEVICEURL, headers = RequestHeader, timeout = 10)
DevicesJSON = Devices.json()

for DeviceIds in DevicesJSON["devices"]:
    if DeviceIds["deviceType"] == "WAVE_PLUS":
        DeviceId = DeviceIds["id"]

        # Query for the devices stats
        Stats = requests.get(url=DEVICEURL + DeviceId +
                             '/latest-samples', headers = RequestHeader, timeout = 10)
        StatsJSON = Stats.json()

        # Format the data for influxDB, adding the deviceId to the output
        Data = StatsJSON["data"]
        Data["deviceid"] = int(DeviceId)

        # Output the data
        print(json.dumps(Data))

    else:
        print("No WAVE PLUS devices found.")
