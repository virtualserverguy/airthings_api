# airthings_api
Query Airthings API for values via telegraf or similar

# Usage
Replace the client ID and client secret with values supplied from airthings. This can be used with telegraf to query values with something as simple as:

```
# Airthings Data
[[inputs.exec]]
  name_suffix = "_airthings"
  commands = ["python3 /scripts/query_airthings.py"]
  timeout = "15s"
  data_format = "json"
```
